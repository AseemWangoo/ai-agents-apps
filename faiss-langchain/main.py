from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import create_retriever_tool
from langchain.agents import create_agent

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

texts = [
    "Apple makes very good computers.",
    "I believe Apple is innovative!",
    "I love apples.",
    "I am a fan of MacBooks.",
    "I enjoy oranges.",
    "I like Lenovo Thinkpads.",
    "I think pears taste very good.",
]


vector_store = FAISS.from_texts(texts=texts, embedding=embeddings)

# print(vector_store.similarity_search("Apples are my favorite food", k=7))

retriever = vector_store.as_retriever(search_kwargs={"k": 3})
retriever_tool = create_retriever_tool(
    retriever=retriever, name="kb_search", description="Search the small product"
)

agent = create_agent(
    model="gpt-4.1-mini",
    tools=[retriever_tool],
    system_prompt=(
        "You are a helpful assistant. For questions about Macs, apples, or laptops, "
        "first call the kb_search tool to retrieve context, then answer succinctly. Maybe you have to use it multiple times before answering."
    ),
)

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "What does the person like and dislike?"}
        ]
    }
)

print(result)
print(result["messages"][-1].content)
