import arxiv

def fetch_arxiv_papers(query: str, max_results: int = 5):
    """
    Fetches papers from ArXiv based on a query.
    """
    print(f"[RAG] Searching ArXiv for: '{query}'...")
    
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = []
    try:
        for result in client.results(search):
            papers_metadata = {
                "id": result.entry_id,
                "title": result.title,
                "summary": result.summary.replace("\n", " "),
                "published": str(result.published),
                "url": result.pdf_url
            }
            results.append(papers_metadata)
    except Exception as e:
        print(f"[RAG] Error fetching ArXiv data: {e}")
        
    print(f"[RAG] Found {len(results)} papers.")
    return results
