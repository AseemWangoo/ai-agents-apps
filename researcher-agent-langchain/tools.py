from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_classic.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime


def save_to_text(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    formatted_text = f"--- Research Output ---\n Timestamp: {timestamp} \n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"


search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search", func=search.run, description="Search the web for information"
)

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_text,
    description="Saves structured research data to a text file.",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)


def safe_wiki_run(query: str) -> str:
    try:
        result = api_wrapper.run(query)
        return result if result else "No Wikipedia result found"
    except Exception as e:
        return f"Wikipedia lookup failed: {e}"


wiki_tool = Tool(
    name="wikipedia",
    func=safe_wiki_run,
    description="Search Wikipedia for factual background.",
)
