from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph

load_dotenv()

llm = init_chat_model(model="claude-haiku-4-5-20251001")


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(state_schema=State)


# Create chatbot node
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# Create Graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

user_input = input("Enter a message: ")
state = graph.invoke({"messages": [{"role": "user", "content": user_input}]})

print(state["messages"][-1].content)

# %% visualize
# from IPython.display import Image, display

# try:
#     png = graph.get_graph().draw_mermaid_png()
#     with open("graph.png", "wb") as f:
#         f.write(png)
#     display(Image(png))
# except Exception:
#     pass