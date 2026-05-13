# AI Agents Apps

1. Researcher-agent-langchain

CLI research assistant built with **LangChain** and **Claude** (`ChatAnthropic`). You enter a topic; a **tool-calling agent** (LangChain classic `AgentExecutor`) can search the web (DuckDuckGo), pull context from Wikipedia, and append results to a local text file. The model is steered to return structured output matching a **Pydantic** schema (topic, summary, sources, tools used).

2. Local AI Agent RAG
   Local **RAG** over restaurant reviews: **Chroma** + **Ollama** embeddings (`mxbai-embed-large`), generation with **Ollama** (`gpt-oss:20b`). `vector.py` builds/refreshes a persisted Chroma DB from `realistic_restaurant_reviews.csv`; `main.py` loops on stdin, retrieves top chunks for each question, and runs a LangChain `ChatPromptTemplate | OllamaLLM` chain.