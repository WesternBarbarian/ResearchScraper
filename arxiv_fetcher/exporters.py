"""Module for exporting arXiv papers data to different formats."""

import json
import csv
from typing import List, Dict, Any
from datetime import datetime

def export_to_json(papers: List[Dict[str, Any]], output_file: str) -> None:
    """Export papers data to JSON file."""
    # Ensure the filename has .json extension
    if not output_file.endswith('.json'):
        output_file += '.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'paper_count': len(papers),
                'export_format_version': '1.0'
            },
            'papers': papers
        }, f, indent=2, ensure_ascii=False)

def export_to_csv(papers: List[Dict[str, Any]], output_file: str) -> None:
    """Export papers data to CSV file."""
    # Ensure the filename has .csv extension
    if not output_file.endswith('.csv'):
        output_file += '.csv'

    # Define CSV headers based on paper structure
    fieldnames = ['title', 'authors', 'published', 'categories', 'summary', 'link']

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for paper in papers:
            # Prepare row data with proper formatting
            row = {
                'title': paper['title'],
                'authors': '; '.join(paper['authors']),
                'published': paper['published'][:10],  # Just the date part
                'categories': ', '.join(paper['categories']),
                'summary': paper['summary'],
                'link': paper['link']
            }
            writer.writerow(row)
