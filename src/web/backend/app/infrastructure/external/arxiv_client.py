"""ArXiv API client."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import re


class ArxivClient:
    """Client for fetching papers from arXiv."""
    
    BASE_URL = "https://arxiv.org/list"
    
    def fetch_papers(self, category: str, num_papers: int = 50) -> List[Dict[str, str]]:
        """Fetch papers from arXiv for a given category."""
        url = f"{self.BASE_URL}/{category}/recent?skip=0&show={num_papers}"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract papers
            papers = []
            articles = soup.select("#articles > dt, #articles > dd")
            
            for i in range(0, len(articles), 2):
                if i + 1 >= len(articles):
                    break
                
                meta_block = articles[i].get_text() if i < len(articles) else ""
                title_block = articles[i + 1] if i + 1 < len(articles) else None
                
                if not title_block:
                    continue
                
                # Extract PDF link
                pdf_match = re.search(r'href="([^"]*\/pdf\/[^"]*)"', str(articles[i]))
                pdf_link = None
                if pdf_match:
                    pdf_path = pdf_match.group(1)
                    pdf_link = f"https://arxiv.org{pdf_path}"
                
                # Extract title
                title_span = title_block.find('span', class_='descriptor', string='Title:')
                if title_span:
                    title_div = title_span.find_next_sibling()
                    if title_div:
                        title = title_div.get_text(strip=True)
                        
                        # Extract ArXiv ID from PDF link
                        arxiv_id = None
                        if pdf_link:
                            arxiv_id_match = re.search(r'/pdf/(\d{4}\.\d{5}(v\d+)?)', pdf_link)
                            if arxiv_id_match:
                                arxiv_id = arxiv_id_match.group(1)
                        
                        if title and pdf_link:
                            papers.append({
                                "title": title,
                                "pdf_link": pdf_link,
                                "arxiv_id": arxiv_id,
                            })
            
            return papers
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch papers from arXiv: {str(e)}")

