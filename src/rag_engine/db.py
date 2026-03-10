import os
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict

# Persist data in a local folder
DB_PATH = "./chroma_db"

class ResearchDB:
    def __init__(self):
        # Initialize Client
        self.client = chromadb.PersistentClient(path=DB_PATH)
        
        # Determine Embedding Function
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("[DB] Using OpenAI Embeddings.")
            embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                api_key=api_key,
                model_name="text-embedding-3-small"
            )
        else:
            print("[DB] ⚠️ OPENAI_API_KEY not found. Falling back to local 'all-MiniLM-L6-v2'.")
            # Default ChromaDB embedding (sentence-transformers)
            embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

        self.collection = self.client.get_or_create_collection(
            name="research_papers",
            embedding_function=embedding_fn
        )

    def ingest_papers(self, papers: List[Dict]):
        """
        Adds a list of paper dictionaries to the database.
        """
        if not papers:
            return

        documents = []
        metadatas = []
        ids = []

        for paper in papers:
            # We use the summary as the content to embed
            documents.append(paper["summary"])
            metadatas.append({
                "title": paper["title"],
                "url": paper["url"],
                "published": paper["published"]
            })
            ids.append(paper["id"])

        # Upsert (update or insert)
        self.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"[DB] Successfully ingested {len(papers)} papers into ChromaDB.")

    def search(self, query: str, n_results: int = 3) -> List[str]:
        """
        Semantic search for relevant papers. 
        Returns a list of formatted strings.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_results = []
        if results['documents']:
            # results['documents'] is a list of lists (one list per query)
            docs = results['documents'][0]
            metas = results['metadatas'][0]
            
            for i, doc in enumerate(docs):
                meta = metas[i]
                formatted = f"Title: {meta['title']}\nSummary: {doc}\nSource: {meta['url']}"
                formatted_results.append(formatted)
                
        return formatted_results

# Singleton instance for easy import
# db = ResearchDB() 
