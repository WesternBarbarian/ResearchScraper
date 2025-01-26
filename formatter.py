"""Formatter for displaying paper information using Rich."""

from rich.console import Console
from rich.table import Table
from rich.text import Text
from typing import List, Dict, Any
from config import MAX_ABSTRACT_LENGTH

class PaperFormatter:
    def __init__(self):
        self.console = Console()

    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text with ellipsis if too long."""
        return text[:max_length] + "..." if len(text) > max_length else text

    def display_papers(self, papers: List[Dict[str, Any]]) -> None:
        """Display papers in a formatted table."""
        if not papers:
            self.console.print("[yellow]No papers found for the specified criteria.[/yellow]")
            return

        # Create table
        table = Table(show_header=True, header_style="bold magenta", 
                     title="Recent arXiv Papers in CS/AI")
        
        table.add_column("Title", style="cyan", no_wrap=False)
        table.add_column("Authors", style="green")
        table.add_column("Published", style="yellow")
        table.add_column("Categories", style="blue")
        table.add_column("Abstract", style="white")

        # Add rows
        for paper in papers:
            table.add_row(
                self._truncate_text(paper['title'], 100),
                self._truncate_text(", ".join(paper['authors']), 50),
                paper['published'][:10],
                ", ".join(paper['categories']),
                self._truncate_text(paper['summary'], MAX_ABSTRACT_LENGTH)
            )

        self.console.print(table)
        self.console.print(f"\nTotal papers found: {len(papers)}")
