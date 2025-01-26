"""Paper downloader module for downloading and organizing arXiv papers as PDFs."""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import arxiv
from pathlib import Path
import re

class PaperDownloader:
    """Downloads and organizes arXiv papers as PDFs."""

    def __init__(self, output_dir: str = "papers"):
        """Initialize with output directory."""
        self.output_dir = Path(output_dir)
        self.download_log = self.output_dir / ".download_log.json"

    def _load_download_log(self) -> Dict:
        """Load the download log to avoid re-downloading papers."""
        if self.download_log.exists():
            with open(self.download_log, 'r') as f:
                return json.load(f)
        return {"papers": {}}

    def _save_download_log(self, log_data: Dict) -> None:
        """Save the download log."""
        with open(self.download_log, 'w') as f:
            json.dump(log_data, f, indent=2)

    def _create_paper_dir(self, paper: Dict) -> Path:
        """Create and return directory path for a paper."""
        # Create sanitized directory name from paper title
        paper_dir_name = "".join(c if c.isalnum() or c in [' ', '-'] else '_' 
                                for c in paper['title'])[:100].strip()
        paper_dir = self.output_dir / paper_dir_name
        paper_dir.mkdir(parents=True, exist_ok=True)
        return paper_dir

    def _extract_arxiv_id_from_link(self, link: str) -> Optional[str]:
        """Extract arXiv ID from a paper link/ID string."""
        # Try to match patterns like arxiv.org/abs/2401.12345 or just 2401.12345
        patterns = [
            r'arxiv\.org/abs/([0-9]+\.[0-9]+v[0-9]+)',  # With version
            r'arxiv\.org/abs/([0-9]+\.[0-9]+)',         # Without version
            r'arxiv\.org/pdf/([0-9]+\.[0-9]+v[0-9]+)',  # PDF with version
            r'arxiv\.org/pdf/([0-9]+\.[0-9]+)',         # PDF without version
            r'^([0-9]{4}\.[0-9]+v[0-9]+)$',            # Raw ID with version
            r'^([0-9]{4}\.[0-9]+)$'                     # Raw ID without version
        ]

        for pattern in patterns:
            if match := re.search(pattern, link):
                return match.group(1)
        return None

    def _get_arxiv_id(self, paper: Dict) -> str:
        """Extract arXiv ID from paper data."""
        # Try to find URLs in paper data
        possible_urls = []

        # Direct fields
        for field in ['url', 'pdf_url', 'entry_id', 'id', 'link']:
            if field in paper and paper[field]:
                possible_urls.append(paper[field])

        # Links array if present
        if 'links' in paper and isinstance(paper['links'], list):
            for link in paper['links']:
                if isinstance(link, dict) and 'href' in link:
                    possible_urls.append(link['href'])
                elif isinstance(link, str):
                    possible_urls.append(link)

        # Try to extract ID from each URL
        for url in possible_urls:
            if arxiv_id := self._extract_arxiv_id_from_link(url):
                return arxiv_id

        # Check for direct arxiv_id field
        if 'arxiv_id' in paper:
            if arxiv_id := self._extract_arxiv_id_from_link(paper['arxiv_id']):
                return arxiv_id
            return paper['arxiv_id']  # Return as-is if it doesn't match patterns

        # If we can't find an ID, raise an error with available fields
        available_fields = ', '.join(paper.keys())
        raise ValueError(f"Could not find arXiv ID for paper: {paper['title']}\n"
                        f"Available fields: {available_fields}\n"
                        "Paper data structure: {json.dumps(paper, indent=2)}")

    def download_papers(self, input_file: str) -> None:
        """Download papers from analyzed JSON file."""
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Load previously downloaded papers
        download_log = self._load_download_log()

        try:
            # Load analyzed papers
            with open(input_file, 'r') as f:
                data = json.load(f)

            papers = data.get('papers', [])
            total_papers = len(papers)

            print(f"\nDownloading {total_papers} papers...")

            for i, paper in enumerate(papers, 1):
                try:
                    arxiv_id = self._get_arxiv_id(paper)
                except ValueError as e:
                    print(f"Error with paper '{paper['title']}': {str(e)}")
                    continue

                # Skip if already downloaded
                if arxiv_id in download_log['papers']:
                    print(f"[{i}/{total_papers}] Already downloaded: {paper['title']}")
                    continue

                print(f"[{i}/{total_papers}] Downloading: {paper['title']}")

                try:
                    # Create paper directory
                    paper_dir = self._create_paper_dir(paper)

                    # Save paper metadata
                    with open(paper_dir / "metadata.json", 'w') as f:
                        json.dump(paper, f, indent=2)

                    # Download PDF using arxiv package
                    search = arxiv.Search(id_list=[arxiv_id])
                    paper_result = next(search.results())
                    paper_result.download_pdf(dirpath=str(paper_dir),
                                           filename="paper.pdf")

                    # Update download log
                    download_log['papers'][arxiv_id] = {
                        'downloaded_at': datetime.now().isoformat(),
                        'title': paper['title'],
                        'directory': str(paper_dir)
                    }

                except Exception as e:
                    print(f"Error downloading {paper['title']}: {str(e)}")
                    continue

            # Save updated download log
            self._save_download_log(download_log)

            print(f"\nDownload complete! Papers saved in: {self.output_dir}")

        except Exception as e:
            print(f"Error processing papers: {str(e)}")
            raise