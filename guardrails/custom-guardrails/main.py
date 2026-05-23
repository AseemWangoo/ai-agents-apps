from typing import Any
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langgraph.runtime import Runtime
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage

load_dotenv()


class ContentFilterMiddleware(AgentMiddleware):
    """Deterministic guardrail: Block requests containing banned keywords."""

    def __init__(self, banned_keywords: list[str]):
        super().__init__()
        self.banned_keywords = [kw.lower() for kw in banned_keywords]

    @hook_config(can_jump_to=["end"])
    def before_agent(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        # Get the first user message
        if not state["messages"]:
            return None

        first_message = state["messages"][0]
        if first_message.type != "human":
            return None

        content = first_message.content.lower()

        # Check for banned keywords
        for keyword in self.banned_keywords:
            if keyword in content:
                # Block execution before any processing
                return {
                    "messages": [
                        {
                            "role": "assistant",
                            "content": "I cannot process requests containing inappropriate content. Please rephrase your request.",
                        },
                    ],
                    "jump_to": "end",
                }

        return None


class SafetyGuardrailMiddleware(AgentMiddleware):
    """Model-based guardrail: Use an LLM to evaluate response safety."""

    def __init__(self):
        super().__init__()
        self.safety_model = init_chat_model("gpt-5.4-mini")

    @hook_config(can_jump_to=["end"])
    def after_agent(self, state: AgentState, runtime: Runtime):
        # Get the final AI response

        if not state["messages"]:
            return None

        last_message = state["messages"][-1]
        if not isinstance(last_message, AIMessage):
            return None

        safety_prompt = f"""Evaluate if this response is safe and appropriate.
        Respond with only 'SAFE' or 'UNSAFE'.
        
        Response: {last_message.content}"""

        result = self.safety_model.invoke([{"role": "user", "content": safety_prompt}])

        if "UNSAFE" in result.content:
            last_message.content = (
                "I cannot provide that response. Please rephrase your request."
            )

        return None


@tool
def search_tool(query: str):
    """Search for information."""
    return f"Results for: {query}"


# for running the before-agent guardrail
agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool],
    middleware=[
        ContentFilterMiddleware(
            banned_keywords=["hack", "exploit", "malware"],
        )
    ],
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "How do I hack into a database?"}]},
)

print("Unsafe request response:")
print(result["messages"][-1].content)


# for running the after-agent guardrail
# agent = create_agent(
#     model="gpt-5.4",
#     tools=[search_tool],
#     middleware=[SafetyGuardrailMiddleware()],
# )


# result = agent.invoke(
#     {"messages": [{"role": "user", "content": "How do I make explosives?"}]},
# )

# print("Unsafe request response:")
# print(result["messages"][-1].content)
