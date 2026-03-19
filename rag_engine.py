import requests
import urllib.parse
from typing import List, Dict

class RAGEngine:
    def __init__(self, max_results: int = 10):
        self.max_results = max_results
        self.arxiv_base_url = "http://export.arxiv.org/api/query"
        
    def search_arxiv(self, query: str) -> List[Dict]:
        """
        Search arXiv for papers matching the query.
        Returns a list of paper metadata.
        """
        print(f"[RAG] Searching arXiv for: {query}")
        
        # Clean and shorten query if needed
        query = query.strip()
        if len(query) > 150:
            query = " ".join(query.split()[:15])
        
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': self.max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(self.arxiv_base_url, params=params, timeout=30)
            response.raise_for_status()
            
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            papers = []
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns)
                summary = entry.find('atom:summary', ns)
                published = entry.find('atom:published', ns)
                authors = entry.findall('atom:author/atom:name', ns)
                link = entry.find('atom:id', ns)
                
                paper = {
                    'title': title.text.strip().replace('\n', ' ') if title is not None else 'N/A',
                    'abstract': summary.text.strip().replace('\n', ' ') if summary is not None else 'N/A',
                    'published': published.text[:10] if published is not None else 'N/A',
                    'authors': [author.text for author in authors] if authors else [],
                    'url': link.text if link is not None else 'N/A'
                }
                papers.append(paper)
            
            print(f"[RAG] Successfully retrieved {len(papers)} papers from arXiv")
            return papers
            
        except Exception as e:
            print(f"[RAG] Error searching arXiv: {e}")
            print(f"[RAG] Attempting simplified search...")
            try:
                simple_query = " ".join(query.split()[:5])
                params['search_query'] = f'all:{simple_query}'
                response = requests.get(self.arxiv_base_url, params=params, timeout=30)
                response.raise_for_status()
                
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                ns = {
                    'atom': 'http://www.w3.org/2005/Atom',
                    'arxiv': 'http://arxiv.org/schemas/atom'
                }
                
                papers = []
                for entry in root.findall('atom:entry', ns):
                    title = entry.find('atom:title', ns)
                    summary = entry.find('atom:summary', ns)
                    published = entry.find('atom:published', ns)
                    authors = entry.findall('atom:author/atom:name', ns)
                    link = entry.find('atom:id', ns)
                    
                    paper = {
                        'title': title.text.strip().replace('\n', ' ') if title is not None else 'N/A',
                        'abstract': summary.text.strip().replace('\n', ' ') if summary is not None else 'N/A',
                        'published': published.text[:10] if published is not None else 'N/A',
                        'authors': [author.text for author in authors] if authors else [],
                        'url': link.text if link is not None else 'N/A'
                    }
                    papers.append(paper)
                
                print(f"[RAG] Fallback successful! Retrieved {len(papers)} papers")
                return papers
                
            except Exception as fallback_error:
                print(f"[RAG] Fallback also failed: {fallback_error}")
                return []

    def analyze_papers(self, papers: List[Dict]) -> List[Dict]:
        """
        Individually analyze each paper and extract:
        - Key contribution
        - Methods used
        - Limitations
        - Relevance score (keyword-based)
        """
        print(f"[RAG] Analyzing {len(papers)} papers individually...")
        analyzed = []

        for idx, paper in enumerate(papers, 1):
            abstract = paper['abstract'].lower()

            # Extract key methods mentioned
            method_keywords = [
                'deep learning', 'neural network', 'cnn', 'rnn', 'transformer',
                'wavelet', 'fourier', 'sparse', 'dictionary learning', 'autoencoder',
                'gan', 'diffusion', 'attention', 'graph neural', 'random forest',
                'support vector', 'principal component', 'blind deconvolution',
                'f-x', 'median filter', 'wiener filter', 'kalman', 'bayesian'
            ]
            found_methods = [m for m in method_keywords if m in abstract]

            # Extract key topics
            topic_keywords = [
                'noise', 'denois', 'signal', 'seismic', 'geophysic', 'subsurface',
                'reflection', 'refraction', 'attenuation', 'velocity', 'inversion',
                'imaging', 'migration', 'interpolation', 'reconstruction'
            ]
            found_topics = [t for t in topic_keywords if t in abstract]

            # Simple relevance score based on keyword hits
            relevance = min(10, len(found_methods) * 2 + len(found_topics))

            analysis = {
                **paper,
                'paper_number': idx,
                'methods_identified': found_methods if found_methods else ['Not explicitly mentioned'],
                'topics_covered': found_topics if found_topics else ['General'],
                'relevance_score': relevance,
                'key_contribution': paper['abstract'][:300]
            }
            analyzed.append(analysis)
            print(f"[RAG] Paper {idx}/{len(papers)} analyzed - Relevance: {relevance}/10 - \"{paper['title'][:60]}...\"")

        return analyzed

    def format_results(self, papers: List[Dict]) -> str:
        """
        Format analyzed papers into a structured readable string.
        """
        if not papers:
            return "No papers found."

        # Sort by relevance score descending
        papers = sorted(papers, key=lambda x: x.get('relevance_score', 0), reverse=True)

        formatted = f"\n{'='*80}\n"
        formatted += f"PAPER ANALYSIS REPORT - {len(papers)} Papers Retrieved & Analyzed\n"
        formatted += f"{'='*80}\n"

        for paper in papers:
            idx = paper['paper_number']
            authors_str = ", ".join(paper['authors'][:3])
            if len(paper['authors']) > 3:
                authors_str += " et al."

            formatted += f"\n[Paper {idx}] \"{paper['title']}\"\n"
            formatted += f"  Authors   : {authors_str}\n"
            formatted += f"  Published : {paper['published']}\n"
            formatted += f"  URL       : {paper['url']}\n"
            formatted += f"  Relevance : {paper['relevance_score']}/10\n"
            formatted += f"  Methods   : {', '.join(paper['methods_identified'])}\n"
            formatted += f"  Topics    : {', '.join(paper['topics_covered'])}\n"
            formatted += f"  Key Point : {paper['key_contribution']}...\n"
            formatted += f"{'-'*80}\n"

        return formatted

    def search_literature(self, query: str) -> str:
        """
        Main search function: fetches + individually analyzes all papers from arXiv.
        """
        papers = self.search_arxiv(query)
        analyzed = self.analyze_papers(papers)
        return self.format_results(analyzed)
