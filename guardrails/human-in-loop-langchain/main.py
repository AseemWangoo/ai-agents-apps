from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()


@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    return f"Email sent to {to} with subject: {subject}"


@tool
def delete_records(table: str, condition: str) -> str:
    """Delete records from the database."""
    return f"Deleted records from {table} where {condition}"


agent = create_agent(
    model="gpt-5.4",
    tools=[search_web, send_email, delete_records],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                # Require approval for sensitive operations
                "send_email": True,
                "delete_records": True,
                # Auto-approve safe operations
                "search_web": False,
            },
        ),
    ],
    checkpointer=InMemorySaver(),
)

# Human-in-the-loop requires a thread ID for persistence
config = {"configurable": {"thread_id": "1"}}

# Agent will pause and wait for approval before executing sensitive tools
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Send an email to the team",
            },
        ]
    },
    config=config,
)

print("=== Agent paused -- awaiting human approval ===")


# Step 2: Human reviews and APPROVES
# result = agent.invoke(
#     Command(resume={"decisions": [{"type": "approve"}]}),
#     config=config,
# )

# print("=== Approved! Final response ===")
# print(result["messages"][-1].content)

# Alternative -- Human REJECTS
config_reject = {"configurable": {"thread_id": "2"}}

agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Delete all records from the database",
            },
        ]
    },
    config=config_reject,
)

rejected_result = agent.invoke(
    Command(
        resume={
            "decisions": [{"type": "reject", "reason": "Too risky, needs DBA review"}]
        }
    ),
    config=config_reject,
)

print("=== Rejected! Final response ===")
print(rejected_result["messages"][-1].content)
