from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from dotenv import load_dotenv
from dataclasses import dataclass
import requests
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


@dataclass
class Context:
    user_id: str


@dataclass
class ResponseFormat:
    summary: str
    temperature_celsius: float
    temperature_fahrenheit: float
    humidity: float


@tool(
    "get_weather",
    description="Return weather information for a given city",
    return_direct=False,
)
def get_weather(city: str):
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    return response.json()


@tool("locate_user", description="Look up a user's city based on the context")
def locate_user(runtime: ToolRuntime[Context]):
    match runtime.context.user_id:
        case "ABC":
            return "Noida"
        case "XYZ":
            return "London"
        case "HJK":
            return "Paris"
        case _:
            return "Unknown"


model = init_chat_model("gpt-4.1-mini", temperature=0.3)
checkpoint = InMemorySaver()


agent = create_agent(
    model="gpt-4.1-mini",
    tools=[get_weather, locate_user],
    system_prompt="You are a helpful weather assistant, who always cracks jokes and is humorous while remaining helpful",
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpoint,
)

config = {"configurable": {"thread_id": 1}}

response = agent.invoke(
    {
        "messages": [{"role": "user", "content": "What is the weather like?"}],
    },
    config=config,
    context=Context(user_id="ABC"),
)

# print(response["structured_response"])
print(response["structured_response"].summary)
# print(response["structured_response"].temperature_celsius)

### This below section shows that the model is aware of the context

config = {
    "configurable": {"thread_id": 1}
}  # If you change the thread_id here, the model wont remember the previous location which is fetched from the user_id

response = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Is this usual?"}],
    },
    config=config,
    context=Context(user_id="ABC"),
)

print(response["structured_response"].summary)


### End
