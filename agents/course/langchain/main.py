import argparse
from datetime import datetime, timezone

from langchain.agents import create_agent
from langchain.tools import tool


@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return a + b


@tool
def current_utc_time() -> str:
    """Return the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def run(prompt: str) -> str:
    agent = create_agent(
        model="openai:gpt-4o-mini",
        tools=[add_numbers, current_utc_time],
        system_prompt=(
            "You are a concise assistant. Use tools when they help improve accuracy."
        ),
    )

    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    messages = result.get("messages", [])

    if messages and hasattr(messages[-1], "content"):
        return str(messages[-1].content)

    return str(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a sample LangChain agent")
    parser.add_argument(
        "--prompt",
        default="What is 12.5 + 7.25? Also tell me the current UTC time.",
        help="Prompt to send to the agent",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(run(args.prompt))
