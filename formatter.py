"""Formatter for displaying paper information using Rich."""

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from typing import List, Dict, Any
from collections import defaultdict
from config import MAX_ABSTRACT_LENGTH

class PaperFormatter:
    def __init__(self):
        self.console = Console()

    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text with ellipsis if too long."""
        return text[:max_length] + "..." if len(text) > max_length else text

    def display_papers(self, papers: List[Dict[str, Any]]) -> None:
        """Display papers in a formatted table, grouped by category combination."""
        if not papers:
            self.console.print("[yellow]No papers found for the specified criteria.[/yellow]")
            return

        # Group papers by their category combination
        grouped_papers = defaultdict(list)
        for paper in papers:
            combo = paper.get('combination', 'Other')
            grouped_papers[combo].append(paper)

        total_papers = 0

        # Display each group in its own table
        for combination, group_papers in grouped_papers.items():
            # Create header for this group
            self.console.print(f"\n[bold cyan]Category Combination: [white]{combination}")
            self.console.print(f"[bold green]Papers found in this category: {len(group_papers)}\n")

            # Create table for this group
            table = Table(show_header=True, header_style="bold magenta",
                        title=f"arXiv Papers - {combination}")

            table.add_column("Title", style="cyan", no_wrap=False)
            table.add_column("Authors", style="green")
            table.add_column("Published", style="yellow")
            table.add_column("Categories", style="blue")
            table.add_column("Abstract", style="white")

            # Add rows for this group
            for paper in group_papers:
                table.add_row(
                    self._truncate_text(paper['title'], 100),
                    self._truncate_text(", ".join(paper['authors']), 50),
                    paper['published'][:10],
                    ", ".join(paper['categories']),
                    self._truncate_text(paper['summary'], MAX_ABSTRACT_LENGTH)
                )

            self.console.print(table)
            self.console.print("\n" + "="*100 + "\n")  # Visual separator
            total_papers += len(group_papers)

        self.console.print(f"\n[bold]Total papers found across all categories: {total_papers}[/bold]")