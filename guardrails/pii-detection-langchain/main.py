from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()


@tool
def customer_service_tool(query: str) -> str:
    """Look up customer information"""
    return f"Customer record found for query: {query}"


agent = create_agent(
    model="gpt-5.4",
    tools=[customer_service_tool],
    middleware=[
        # Redact emails in user input before sending to model
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True,
        ),
        # Mask credit cards in user input
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True,
        ),
        # Block API keys - raise error if detected
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
            apply_to_input=True,
        ),
    ],
)

# When user provides PII, it will be handled according to the strategy
try:
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "My email is john.doe@example.com and card is 5105-1051-0510-5100. Here is my key: sk-abcdefghijklmnopqrstuvwxyz123456",
                }
            ]
        }
    )
    print(result["messages"][-1].content)
except Exception as e:
    print(f"Blocked as expected: {e}")
