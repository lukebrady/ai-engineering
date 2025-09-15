from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, VisitWebpageTool
from tools import calculate_cargo_travel_time

model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct", provider="together")

task = """Find all Batman filming locations in the world, calculate the time to transfer via cargo plane to here (we're in Gotham, 40.7128° N, 74.0060° W), and return them to me as a pandas dataframe.
Also give me some supercar factories with the same cargo plane transfer time."""

agent = CodeAgent(
    model=model,
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool(), calculate_cargo_travel_time],
    additional_authorized_imports=["pandas"],
)

agent.planning_interval = 4

detailed_report = agent.run(f"""
You're an expert analyst. You make comprehensive reports after visiting many websites.
Don't hesitate to search for many queries at once in a for loop.
For each data point that you find, visit the source url to confirm numbers.

{task}
""")

print(detailed_report)
