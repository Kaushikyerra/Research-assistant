# 👤 Member 1: The Knowledge Engineer (RAG & Data)

**Role**: You are responsible for the "eyes and ears" of the agent. You will build the pipeline that fetches scientific literature and stores it in a vector database for retrieval.

## 🎯 Objectives
1.  **Sourcing**: Fetch papers from ArXiv (and optionally Semantic Scholar).
2.  **Storage**: Store paper summaries/abstracts in ChromaDB.
3.  **Retrieval**: Create a tool `search_literature(query)` that the Agent can call.

## 🛠️ Your Workspace
*   **Directory**: `src/rag_engine/`
*   **Key Files**:
    *   `src/rag_engine/retriever.py`: Main logic for fetching and searching.
    *   `src/rag_engine/db.py`: ChromaDB setup and ingestion logic.

## 📝 Step-by-Step Instructions

### Step 1: Install & Setup
Ensure `requirements.txt` is installed.
```bash
pip install -r requirements.txt
```

### Step 2: Implement ArXiv Search
Create a function in `retriever.py` that uses the `arxiv` python package.
*   **Input**: Query string (e.g., "Generative AI in Biology").
*   **Output**: List of dictionaries (Title, Abstract, URL, Published Date).
*   **Limit**: Default to fetching top 5-10 papers.

### Step 3: Setup ChromaDB
In `db.py`:
*   Initialize `chromadb.PersistentClient(path="./chroma_db")`.
*   Create a collection named `research_papers`.
*   Use `OpenAIEmbeddings` (or a local HuggingFace equivalent if API keys are an issue) for the embedding function.

### Step 4: The Ingestion Function
Write a function `ingest_papers(papers)` that:
1.  Takes the list of papers from Step 2.
2.  Adds them to your ChromaDB collection.
3.  Use the Paper URL as the unique `id`.
4.  Store "Title" and "Date" as metadata.
5.  Store "Abstract" as the document content.

### Step 5: The Tool for the Agent
Expose a final function `get_context(query) -> str` that:
1.  Searches ChromaDB for the query.
2.  Returns a formatted string of the top 3 matches to be fed into the LLM.

---
**Definition of Done**:
You can run a script that searches for "Black Holes", saves results to DB, and then successfully queries the DB to retrieve them.
