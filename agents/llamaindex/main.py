import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env.secure"))

from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent
from llama_index.core.workflow import Context

from tools import add, subtract, multiply, divide


# Define async function
async def main():
    # Initialize llm
    llm = HuggingFaceInferenceAPI(
        model_name="Qwen/Qwen2.5-Coder-32B-Instruct",
        token=os.getenv("HUGGING_FACE_TOKEN"),
        provider="auto",
    )

    calculator_agent = ReActAgent(
        name="Calculator",
        description="A calculator agent that can add, subtract, multiply, and divide numbers.",
        system_prompt="You are a calculator agent that can add, subtract, multiply, and divide numbers.",
        tools=[add, subtract, multiply, divide],
        llm=llm,
    )

    # Initalize agent
    agent = AgentWorkflow(
        agents=[calculator_agent],
    )

    ctx = Context(agent)

    # Run agent
    response = await agent.run(
        user_msg="Add 2 and 3 and multiply the result by 4 then divide the result by 2",
        ctx=ctx,
    )
    print(response)


# Run async function
if __name__ == "__main__":
    asyncio.run(main())
