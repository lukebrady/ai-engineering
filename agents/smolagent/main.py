import os
import dotenv

dotenv.load_dotenv(dotenv_path=".env.secure")

from huggingface_hub import login
from langfuse import get_client
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, ToolCallingAgent, tool


HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

login(token=HUGGING_FACE_TOKEN)

langfuse_client = get_client()


if langfuse_client.auth_check():
    print("Langfuse client authenticated")
else:
    print("Langfuse client not authenticated")

SmolagentsInstrumentor().instrument()


@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion (str): The type of occasion for the party. Allowed values are:
                        - "casual": Menu for casual party.
                        - "formal": Menu for formal party.
                        - "superhero": Menu for superhero party.
                        - "custom": Custom menu.
    """
    if occasion == "casual":
        return "The best menu for casual party is pizza."
    elif occasion == "formal":
        return "The best menu for formal party is steak."
    elif occasion == "superhero":
        return "The best menu for superhero party is superhero pizza."
    else:
        return "The best menu for custom party is custom menu."


def music_agent():
    prompt = """
    Search for the best music recommendations for a Bruce Wayne's party.
    """
    return ToolCallingAgent(
        model=InferenceClientModel(),
        tools=[DuckDuckGoSearchTool()],
    ).run(prompt)


def menu_agent():
    prompt = """
    Suggest a menu for a Bruce Wayne's party.
    """
    return CodeAgent(
        model=InferenceClientModel(),
        tools=[suggest_menu],
    ).run(prompt)


def schedule_agent():
    prompt = """
    Alfred needs to prepare for the party. Here are the tasks:
    1. Prepare the drinks - 30 minutes
    2. Decorate the mansion - 60 minutes
    3. Set up the menu - 45 minutes
    4. Prepare the music and playlist - 45 minutes

    If we start right now, at what time will the party be ready?
    """
    return CodeAgent(
        model=InferenceClientModel(),
        tools=[],
        additional_authorized_imports=["datetime"],
    ).run(prompt)


def response_agent(music: str, menu: str, schedule: str):
    prompt = """
    Describe Bruce Wayne's party in a way that is engaging and interesting. 
    Ensure to list out the menu items in the response.
    For music, please provide the name of the song and the artist.
    For schedule, please provide the time in the format of HH:MM:SS.
    Music: {music}, Menu: {menu}, Schedule: {schedule}
    """
    return CodeAgent(
        model=InferenceClientModel(),
        tools=[],
    ).run(prompt.format(music=music, menu=menu, schedule=schedule))


def main():
    # First, we need to get the results from the music and menu agents.
    music_result = music_agent()
    menu_result = menu_agent()

    # Then, we schedule the party.
    schedule_result = schedule_agent()

    # Then, we synthesize the results into a response.
    response_result = response_agent(music_result, menu_result, schedule_result)
    print(response_result)


if __name__ == "__main__":
    main()
