from langchain.tools import tool
from langchain.agents import create_agent

from dotenv import load_dotenv
import requests

load_dotenv()


@tool(
    "get_weather",
    description="Return weather information for a given city",
    return_direct=False,
)
def get_weather(city: str):
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    return response.json()


# create agent
agent = create_agent(
    model="gpt-4.1-mini",
    tools=[get_weather],
    system_prompt="You are a helpful weather assistant, who always cracks jokes and is humorous while remaining helpful",
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in Noida?"}]}
)

print(response["messages"][-1].content)

## For Streaming

# for chunk in agent.stream(
#     {"messages": [{"role": "user", "content": "What is the weather in Noida?"}]},
#     stream_mode="messages",
# ):
#     message_chunk, metadata = chunk
#     if message_chunk.content:
#         print(message_chunk.content, end="", flush=True)
