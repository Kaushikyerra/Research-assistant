"""
RAG Engine Module - Member 1's Work
Handles paper retrieval from ArXiv and ChromaDB storage.
"""

from .retriever import fetch_arxiv_papers
from .db import ResearchDB

__all__ = [
    'fetch_arxiv_papers',
    'ResearchDB'
]
