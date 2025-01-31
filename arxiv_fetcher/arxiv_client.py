"""ArXiv API client for fetching research papers."""

import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time
from typing import List, Dict, Any, Optional

from .config import ARXIV_API_URL, API_DELAY, DEFAULT_CATEGORY

class ArxivClient:
    def __init__(self):
        self.last_request_time = 0

    def _respect_rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < API_DELAY:
            time.sleep(API_DELAY - time_since_last_request)
        self.last_request_time = time.time()

    def _safe_get_text(self, element: Optional[ET.Element], namespace: Dict[str, str], path: str) -> str:
        """Safely get text from XML element."""
        if element is None:
            return ""
        found = element.find(path, namespace)
        return found.text.strip() if found is not None and found.text is not None else ""

    def fetch_papers(self, days: int, max_results: int, categories: List[tuple] = None) -> List[Dict[str, Any]]:
        """Fetch papers from arXiv API.
        
        Args:
            days: Number of days to look back
            max_results: Maximum number of results to return
            categories: List of tuples, each containing (cat1, cat2, operator)
                       where operator is 'AND' or 'OR'. If None, uses DEFAULT_CATEGORY
        """
        self._respect_rate_limit()

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        all_papers = []

        # If no categories specified, use default
        if not categories:
            categories = [(DEFAULT_CATEGORY, None, 'AND')]

        # Query for each combination of categories
        for combo in categories:
            cat1, cat2, operator = combo if len(combo) == 3 else (*combo, 'AND')
            
            # Construct query based on whether we have one or two categories
            if cat2:
                query = f'cat:{cat1} {operator} cat:{cat2}'
            else:
                query = f'cat:{cat1}'
                
            query_params = {
                'search_query': query,
                'start': 0,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }

            try:
                # Make request
                url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(query_params)}"
                response = urllib.request.urlopen(url)
                data = response.read().decode('utf-8')

                # Parse XML response
                root = ET.fromstring(data)
                namespace = {'atom': 'http://www.w3.org/2005/Atom'}

                for entry in root.findall('atom:entry', namespace):
                    # Extract paper details
                    paper = {
                        'title': self._safe_get_text(entry, namespace, 'atom:title'),
                        'authors': [
                            self._safe_get_text(author, namespace, 'atom:name')
                            for author in entry.findall('atom:author', namespace)
                        ],
                        'published': self._safe_get_text(entry, namespace, 'atom:published'),
                        'summary': self._safe_get_text(entry, namespace, 'atom:summary'),
                        'link': self._safe_get_text(entry, namespace, 'atom:id'),
                        'categories': [
                            cat.get('term', '')
                            for cat in entry.findall('atom:category', namespace)
                        ]
                    }

                    # Filter by date
                    pub_date = datetime.strptime(paper['published'][:10], '%Y-%m-%d')
                    if start_date <= pub_date <= end_date:
                        all_papers.append(paper)

            except (urllib.error.URLError, ET.ParseError) as e:
                raise Exception(f"Error fetching papers from arXiv: {str(e)}")

        return all_papers
