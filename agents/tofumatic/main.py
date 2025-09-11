import dotenv
import os
import json
import signal
import sys
import time
import logging
from typing import List, Dict, Optional, Any
from functools import wraps

from openai import OpenAI
from colorama import Fore, Style, init

from tools import tool_definitions, tools_map

from prompts import INFRASTRUCTURE_ENGINEER_PROMPT, CODE_PLANNING_PROMPT, PROMPT_GEN_PROMPT

dotenv.load_dotenv(dotenv_path=".env.secure")

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tofumatic.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Function {func.__name__} failed after {max_retries} attempts: {e}")
                        raise
                    
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def validate_json_response(response: str, expected_keys: Optional[List[str]] = None) -> Optional[Dict]:
    try:
        data = json.loads(response)
        if expected_keys:
            missing_keys = [key for key in expected_keys if key not in data]
            if missing_keys:
                logger.error(f"Missing required keys in response: {missing_keys}")
                return None
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON response: {e}")
        return None

XAI_API_KEY = os.getenv("XAI_API_KEY")

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

@retry_with_backoff(max_retries=3, base_delay=1.0)
def prompt_agent(prompt: str) -> Optional[Dict]:
    logger.info(f"Starting prompt_agent with input: {prompt[:100]}...")
    prompt_response = ""
    
    try:
        response = client.chat.completions.create(
            model="grok-4-0709",
            messages=[
                {"role": "system", "content": PROMPT_GEN_PROMPT},
                {"role": "user", "content": prompt},
            ],
            stream=True,
        )
        
        for chunk in response:
            if hasattr(chunk, "choices") and chunk.choices:
                delta = chunk.choices[0].delta
                if hasattr(delta, "content") and delta.content:
                    prompt_response += delta.content
                    print(delta.content, end="", flush=True)
        
        print()  # Add newline after streaming
        
        # Validate the JSON response
        result = validate_json_response(prompt_response, expected_keys=["continue"])
        if result is None:
            logger.error(f"Invalid response from prompt_agent: {prompt_response[:200]}...")
            return {"continue": False, "prompt": "", "error": "Invalid JSON response"}
        
        logger.info(f"prompt_agent completed successfully. Continue: {result.get('continue', False)}")
        return result
        
    except Exception as e:
        logger.error(f"Error in prompt_agent: {e}")
        raise

@retry_with_backoff(max_retries=3, base_delay=1.0)
def code_planning_agent(project_description: str) -> List[Dict]:
    logger.info(f"Starting code_planning_agent with description: {project_description[:100]}...")
    code_plan = ""
    
    try:
        response = client.chat.completions.create(
            model="grok-code-fast-1",
            messages=[
                {"role": "system", "content": CODE_PLANNING_PROMPT},
                {"role": "user", "content": project_description},
            ],
            tools=tool_definitions,
            tool_choice="auto",
            stream=True,
        )
        
        for chunk in response:
            if hasattr(chunk, "choices") and chunk.choices:
                delta = chunk.choices[0].delta
                if hasattr(delta, "content") and delta.content:
                    code_plan += delta.content
                    print(delta.content, end="", flush=True)
        
        print()
        
        # Validate and parse the JSON response
        if not code_plan.strip():
            logger.warning("Empty response from code_planning_agent")
            return []
        
        try:
            result = json.loads(code_plan)
            if not isinstance(result, list):
                logger.error(f"Expected list but got {type(result)} from code_planning_agent")
                return []
            
            # Validate each step has required structure
            valid_steps = []
            for i, step in enumerate(result):
                if isinstance(step, dict):
                    valid_steps.append(step)
                else:
                    logger.warning(f"Step {i} is not a dictionary, skipping: {step}")
            
            logger.info(f"code_planning_agent completed successfully with {len(valid_steps)} valid steps")
            return valid_steps
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format from code_planning_agent: {e}")
            logger.error(f"Raw response: {code_plan[:500]}...")
            return []
            
    except Exception as e:
        logger.error(f"Error in code_planning_agent: {e}")
        raise

@retry_with_backoff(max_retries=2, base_delay=1.0)
def infrastructure_engineer_agent(code_plan: List[Dict]) -> bool:
    logger.info(f"Starting infrastructure_engineer_agent with {len(code_plan)} steps")
    
    if not code_plan:
        logger.warning("Empty code plan provided to infrastructure_engineer_agent")
        return False
    
    messages = [
        {"role": "system", "content": INFRASTRUCTURE_ENGINEER_PROMPT},
    ]
    
    try:
        for step_index, step in enumerate(code_plan):
            logger.info(f"Processing step {step_index + 1}/{len(code_plan)}: {str(step)[:100]}...")
            
            if not isinstance(step, dict):
                logger.warning(f"Skipping invalid step {step_index + 1}: not a dictionary")
                continue
            
            messages.append({"role": "user", "content": json.dumps(step)})
            
            try:
                response = client.chat.completions.create(
                    model="grok-code-fast-1",
                    messages=messages,
                    tools=tool_definitions,
                    tool_choice="auto",
                    stream=True,
                )
                
                response_content = ""
                for chunk in response:
                    if hasattr(chunk, "choices") and chunk.choices:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, "content") and delta.content:
                            response_content += delta.content
                            print(delta.content, end="", flush=True)
                        
                        if hasattr(delta, "tool_calls") and delta.tool_calls:
                            for tool_call in delta.tool_calls:
                                if not _handle_tool_call(tool_call, messages):
                                    logger.warning(f"Tool call failed or was skipped in step {step_index + 1}")
                
                print()  # Add newline after streaming
                
                if response_content:
                    messages.append({"role": "assistant", "content": response_content})
                    
            except Exception as e:
                logger.error(f"Error processing step {step_index + 1}: {e}")
                print(f"\n{Fore.RED}Error processing step {step_index + 1}: {e}{Style.RESET_ALL}")
                continue
        
        logger.info("infrastructure_engineer_agent completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Fatal error in infrastructure_engineer_agent: {e}")
        print(f"\n{Fore.RED}Fatal error in infrastructure engineer: {e}{Style.RESET_ALL}")
        return False

def _handle_tool_call(tool_call, messages: List[Dict]) -> bool:
    try:
        print(f"\n{Fore.CYAN}Tool Call: {tool_call.function.name}{Style.RESET_ALL}")
        print(f"Arguments: {tool_call.function.arguments}")
        
        try:
            answer = input("Do you want to call this tool? (y/n) ")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            return False
        
        if answer.lower() == "y":
            function_name = tool_call.function.name
            
            if function_name not in tools_map:
                logger.error(f"Unknown tool: {function_name}")
                print(f"{Fore.RED}Error: Unknown tool '{function_name}'{Style.RESET_ALL}")
                return False
            
            try:
                function_args = json.loads(tool_call.function.arguments)
                result = tools_map[function_name](**function_args)
                print(f"{Fore.GREEN}Tool result: {result}{Style.RESET_ALL}")
                
                messages.append({
                    "role": "assistant", 
                    "content": json.dumps(result)
                })
                return True
                
            except json.JSONDecodeError as e:
                logger.error(f"Invalid tool arguments JSON: {e}")
                print(f"{Fore.RED}Error: Invalid tool arguments JSON{Style.RESET_ALL}")
                return False
            except Exception as e:
                logger.error(f"Tool execution failed: {e}")
                print(f"{Fore.RED}Tool execution failed: {e}{Style.RESET_ALL}")
                return False
        else:
            print("Skipping tool call.")
            return True
            
    except Exception as e:
        logger.error(f"Error handling tool call: {e}")
        return False

def opentofu_agent(module_name: str):
    messages = [
        {"role": "system", "content": OPENTOFU_AGENT_PROMPT},
        {"role": "user", "content": module_name},
    ]
    response = client.chat.completions.create(
        model="grok-code-fast-1",
        messages=messages,
    )
    return response.choices[0].message.content

def main():
    logger.info("Starting tofumatic agent system")
    print(f"{Fore.GREEN}🤖 Tofumatic Agent System Started{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Logs are being written to: tofumatic.log{Style.RESET_ALL}")
    
    session_count = 0
    
    while True:
        session_count += 1
        logger.info(f"Starting session {session_count}")
        
        try:
            user_input = input(f"{Fore.YELLOW}tofumatic{Style.RESET_ALL} ■ ")
            
            if not user_input.strip():
                print(f"{Fore.YELLOW}Please provide a valid input.{Style.RESET_ALL}")
                continue
                
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print(f"{Fore.GREEN}Goodbye! 👋{Style.RESET_ALL}")
                logger.info("User requested exit")
                break
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Operation cancelled by user. Goodbye! 👋{Style.RESET_ALL}")
            logger.info("User interrupted with Ctrl+C")
            return
        
        # Step 1: Process prompt with fallback
        try:
            logger.info("Calling prompt_agent")
            prompt_result = prompt_agent(user_input)
            
            if prompt_result is None:
                print(f"{Fore.RED}❌ Failed to process your prompt. Please try again.{Style.RESET_ALL}")
                continue
                
            if not prompt_result.get("continue", False):
                print(f"{Fore.YELLOW}ℹ️  This prompt is not related to OpenTofu. Please provide an OpenTofu-related request.{Style.RESET_ALL}")
                continue
                
            project_description = prompt_result.get("prompt", user_input)
            
        except Exception as e:
            logger.error(f"prompt_agent failed: {e}")
            print(f"{Fore.RED}❌ Error processing prompt: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Falling back to using your input directly...{Style.RESET_ALL}")
            project_description = user_input
        
        # Step 2: Generate code plan with fallback
        try:
            logger.info("Calling code_planning_agent")
            plan_code = code_planning_agent(project_description)
            
            if not plan_code:
                print(f"{Fore.RED}❌ Failed to generate a valid code plan. Skipping to next prompt.{Style.RESET_ALL}")
                continue
                
        except Exception as e:
            logger.error(f"code_planning_agent failed: {e}")
            print(f"{Fore.RED}❌ Error generating code plan: {e}{Style.RESET_ALL}")
            continue
        
        # Step 3: Execute infrastructure engineering with fallback
        try:
            logger.info("Calling infrastructure_engineer_agent")
            success = infrastructure_engineer_agent(plan_code)
            
            if success:
                print(f"\n{Fore.GREEN}✅ Session {session_count} completed successfully!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}⚠️  Session {session_count} completed with some issues. Check the logs for details.{Style.RESET_ALL}")
                
        except Exception as e:
            logger.error(f"infrastructure_engineer_agent failed: {e}")
            print(f"\n{Fore.RED}❌ Error in infrastructure engineering: {e}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")  # Session separator
    

    
    #for chunk in response:
    #    if hasattr(chunk, "choices") and chunk.choices:
    #        delta = chunk.choices[0].delta
    #        if hasattr(delta, "content") and delta.content:
    #            print(delta.content, end="", flush=True)
    #    if hasattr(delta, "tool_calls") and delta.tool_calls:
    #        for tool_call in delta.tool_calls:
    #            print(tool_call)
    #            answer = input("Do you want to call this tool? (y/n)")
    #            if answer == "y":
    #                function_name = tool_call.function.name
    #                function_args = json.loads(tool_call.function.arguments)
    #                result = tools_map[function_name](**function_args)
    #                print(result)
    #            else:
    #                print("Skipping tool call.")
    #print()  # for newline after streaming


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting gracefully...")
        sys.exit(0)
