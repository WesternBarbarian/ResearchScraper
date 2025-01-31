"""Format and display paper information."""

from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from .config import MAX_ABSTRACT_LENGTH

class PaperFormatter:
    def __init__(self):
        self.console = Console()

    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length."""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."

    def display_papers(self, papers: List[Dict[str, Any]]) -> None:
        """Display papers in a formatted table."""
        if not papers:
            self.console.print(Panel("No papers found matching the criteria.", 
                                   title="Results", 
                                   border_style="yellow"))
            return

        # Print summary
        self.console.print(Panel(f"Found {len(papers)} papers", 
                               title="Summary", 
                               border_style="green"))

        # Create and populate table
        table = Table(title="Recent arXiv Papers", 
                     show_lines=True, 
                     expand=True)
        
        table.add_column("Title", style="cyan", no_wrap=False)
        table.add_column("Authors", style="green")
        table.add_column("Published", style="yellow")
        table.add_column("Categories", style="magenta")


    def display_categories(self, categories: Dict[str, str]) -> None:
        """Display arXiv categories in a formatted table."""
        table = Table(title="arXiv Categories", show_lines=True, expand=True)
        table.add_column("Code", style="cyan")
        table.add_column("Description", style="green")

        for code, description in sorted(categories.items()):
            table.add_row(code, description)

        self.console.print(table)


        table.add_column("Summary", style="white")

        for paper in papers:
            table.add_row(
                self._truncate_text(paper['title'], 100),
                self._truncate_text(", ".join(paper['authors']), 50),
                paper['published'][:10],
                ", ".join(paper['categories']),
                self._truncate_text(paper['summary'], MAX_ABSTRACT_LENGTH)
            )

        self.console.print(table)
