import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from rag_engine.retriever import fetch_arxiv_papers
from rag_engine.db import ResearchDB

def verify_rag_pipeline(topic="Generative AI"):
    print(f"--- 🧪 Starting RAG Verification for topic: '{topic}' ---")

    # 1. Fetch Papers
    print("\n[Step 1] Fetching papers from ArXiv...")
    try:
        papers = fetch_arxiv_papers(query=topic, max_results=5)
        if not papers:
            print("❌ No papers found. Check network or query.")
            return
        
        print(f"✅ Fetched {len(papers)} papers:")
        for p in papers:
            print(f"   - {p['title']} ({p['published']})")
            
    except Exception as e:
        print(f"❌ Error fetching papers: {e}")
        return

    # 2. Initialize DB
    print("\n[Step 2] Initializing ChromaDB...")
    try:
        # Check for API Key if using OpenAI (default in db.py)
        if not os.getenv("OPENAI_API_KEY"):
            print("⚠️  WARNING: OPENAI_API_KEY is not set.")
            print("   The embedding process usually requires this key.")
            print("   If ingestion fails, set the key or modify db.py to use a local model.")
            
        db = ResearchDB()
        print("✅ DB Initialized.")
    except Exception as e:
        print(f"❌ Error initializing DB: {e}")
        return

    # 3. Ingest Data
    print("\n[Step 3] Ingesting papers...")
    try:
        db.ingest_papers(papers)
        print("✅ Ingestion requested.")
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        print("   (This is likely due to missing API Key or invalid embedding configuration)")
        return

    # 4. Verify Retrieval
    print("\n[Step 4] Verifying Retrieval (Querying DB)...")
    try:
        results = db.search(query=topic, n_results=2)
        if results:
            print("✅ Retrieval Successful! Found context:")
            for i, res in enumerate(results):
                print(f"   Result {i+1}: {res[:100]}...") # Print first 100 chars
        else:
            print("⚠️  No results returned. Ingestion might have failed silently or DB is empty.")
    except Exception as e:
        print(f"❌ Error during search: {e}")

    print("\n--- 🏁 Verification Verification Complete ---")

if __name__ == "__main__":
    # Allow passing topic via CLI
    topic = sys.argv[1] if len(sys.argv) > 1 else "Agentic workflows"
    verify_rag_pipeline(topic)
