
"""Paper summarizer module that uses OpenAI to generate summaries of parsed papers."""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from openai import OpenAI

# Initialize OpenAI client
openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class PaperSummarizer:
    """Paper summarizer for generating summaries using OpenAI."""
    
    def __init__(self, papers_dir: str = "papers", output_file: str = "paper_summaries.json"):
        """Initialize with papers directory and output file."""
        self.papers_dir = Path(papers_dir)
        self.output_file = Path(output_file)
        
    def load_existing_summaries(self) -> Dict:
        """Load existing summaries if available."""
        if self.output_file.exists():
            with open(self.output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"summaries": {}, "last_updated": None}
        
    def save_summaries(self, summaries: Dict) -> None:
        """Save summaries to output file."""
        summaries["last_updated"] = datetime.now().isoformat()
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, indent=2)
            
    def get_paper_content(self, paper_title: str) -> Optional[str]:
        """Get paper content from markdown file."""
        paper_dir = self.papers_dir / paper_title
        markdown_file = paper_dir / "parsed_paper.md"
        
        if not markdown_file.exists():
            return None
            
        with open(markdown_file, 'r', encoding='utf-8') as f:
            return f.read()
            
    def summarize_paper(self, content: str) -> str:
        """Generate summary using OpenAI."""
        prompt = f"""Please provide a concise summary of this academic paper, focusing on:
1. Main objectives
2. Key methodologies
3. Principal findings
4. Significant implications

Paper content:
{content[:15000]}  # Limit content length for API
"""
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    def process_papers(self, titles: Optional[List[str]] = None, date: Optional[str] = None) -> Dict[str, str]:
        """Process papers by titles or date."""
        if not titles and not date:
            raise ValueError("Either titles or date must be provided")
            
        summaries_data = self.load_existing_summaries()
        if date:
            # Load download log to get papers by date
            log_file = self.papers_dir / ".download_log.json"
            if not log_file.exists():
                raise FileNotFoundError("Download log not found")
                
            with open(log_file, 'r') as f:
                log_data = json.load(f)
                
            titles = [
                data["directory"].split("/")[-1]
                for data in log_data.get("papers", {}).values()
                if data["downloaded_at"].startswith(date)
            ]
            
        for title in titles:
            if title in summaries_data["summaries"]:
                print(f"Summary already exists for: {title}")
                continue
                
            content = self.get_paper_content(title)
            if not content:
                print(f"Error: Markdown file not found for paper: {title}")
                continue
                
            try:
                summary = self.summarize_paper(content)
                summaries_data["summaries"][title] = {
                    "summary": summary,
                    "generated_at": datetime.now().isoformat()
                }
                print(f"Generated summary for: {title}")
            except Exception as e:
                print(f"Error summarizing paper {title}: {str(e)}")
                
        self.save_summaries(summaries_data)
        return summaries_data
