
"""Paper parser module for parsing downloaded papers using LlamaParse."""

import os
import json
from datetime import datetime
from pathlib import Path
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

class PaperParser:
    """Paper parser for processing downloaded PDFs using LlamaParse."""

    def __init__(self, papers_dir: str = "papers"):
        """Initialize with papers directory."""
        self.api_key = os.environ.get("LLAMA_CLOUD_API_KEY")
        if not self.api_key:
            raise ValueError("LLAMA_CLOUD_API_KEY not found in environment variables")
        
        self.papers_dir = Path(papers_dir)
        self.log_file = self.papers_dir / ".download_log.json"
        self.parser = LlamaParse(api_key=self.api_key, result_type="markdown")
        
    def load_download_log(self):
        """Load the download log file."""
        if not self.log_file.exists():
            return {}
        with open(self.log_file, 'r') as f:
            return json.load(f)
            
    def get_papers_by_date(self, date_str=None):
        """Get papers downloaded on a specific date."""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
            
        log_data = self.load_download_log()
        return {
            paper_id: data 
            for paper_id, data in log_data.get('papers', {}).items()
            if data['downloaded_at'].startswith(date_str)
        }
        
    def get_papers_by_titles(self, titles):
        """Get papers by their titles (folder names)."""
        log_data = self.load_download_log()
        return {
            paper_id: data
            for paper_id, data in log_data.get('papers', {}).items()
            if any(title.lower() in data['directory'].lower() for title in titles)
        }
        
    def parse_papers(self, papers_data):
        """Parse the specified papers using LlamaParse."""
        for paper_id, data in papers_data.items():
            paper_dir = Path(data['directory'])
            pdf_path = paper_dir / 'paper.pdf'
            output_path = paper_dir / 'parsed_paper.md'
            
            if not pdf_path.exists():
                print(f"PDF not found for paper: {data['title']}")
                continue
                
            try:
                print(f"Parsing paper: {data['title']}")
                file_extractor = {".pdf": self.parser}
                documents = SimpleDirectoryReader(
                    input_files=[str(pdf_path)],
                    file_extractor=file_extractor
                ).load_data()
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    for doc in documents:
                        f.write(doc.text + '\n\n')
                        
                print(f"Successfully parsed and saved to: {output_path}")
                
            except Exception as e:
                print(f"Error parsing paper {data['title']}: {str(e)}")

def run_parser(titles=None, date=None):
    """Run the parser with specified titles or date."""
    try:
        parser = PaperParser()
        if titles:
            papers = parser.get_papers_by_titles(titles)
        else:
            papers = parser.get_papers_by_date(date)
            
        if not papers:
            print("No matching papers found")
            return
            
        parser.parse_papers(papers)
        
    except Exception as e:
        print(f"Error: {str(e)}")
