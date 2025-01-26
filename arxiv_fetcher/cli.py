"""Command line interface for the ArXiv paper fetcher."""

import sys
import argparse
from typing import Optional
from datetime import datetime

from .config import CACHE_FILE, CACHE_DURATION, MAX_RESULTS
from .cache_manager import CacheManager
from .arxiv_client import ArxivClient
from .formatter import PaperFormatter
from .exporters import export_to_json, export_to_csv
from .paper_analyzer import analyze_papers

def validate_days(days: int) -> bool:
    """Validate the number of days input."""
    return 1 <= days <= 30

def get_cache_key(days: int) -> str:
    """Generate cache key based on parameters."""
    return f"papers_{days}_{datetime.now().strftime('%Y-%m-%d')}"

def run_fetcher(days: Optional[int] = None, export_json: Optional[str] = None, export_csv: Optional[str] = None) -> None:
    """Main function to fetch and display papers."""
    # Use provided days or default
    actual_days = days or 7

    # Validate input
    if not validate_days(actual_days):
        print("Error: Days must be between 1 and 30")
        sys.exit(1)

    # Initialize components
    cache_manager = CacheManager(CACHE_FILE, CACHE_DURATION)
    arxiv_client = ArxivClient()
    formatter = PaperFormatter()

    try:
        # Check cache first
        cache_key = get_cache_key(actual_days)
        cached_data = cache_manager.get(cache_key)

        if cached_data is None:
            # Fetch new data if not in cache
            papers = arxiv_client.fetch_papers(actual_days, MAX_RESULTS)
            cache_manager.set(cache_key, papers)
        else:
            papers = cached_data

        # Export if requested
        if export_json:
            export_to_json(papers, export_json)
            print(f"Papers exported to JSON: {export_json}")

        if export_csv:
            export_to_csv(papers, export_csv)
            print(f"Papers exported to CSV: {export_csv}")

        # Display results if no export options were specified
        if not (export_json or export_csv):
            formatter.display_papers(papers)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def run_analyzer(input_file: str, output_file: str, min_relevance_score: float) -> None:
    """Run the paper analyzer on the input file."""
    try:
        analyze_papers(input_file, output_file, min_relevance_score)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main() -> None:
    """Entry point for command line interface."""
    parser = argparse.ArgumentParser(description='ArXiv paper fetcher and analyzer')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Fetch command
    fetch_parser = subparsers.add_parser('fetch', help='Fetch recent CS/AI papers from arXiv')
    fetch_parser.add_argument('--days', type=int, default=7,
                          help='Number of days to look back (1-30)')
    fetch_parser.add_argument('--export-json', type=str, metavar='FILENAME',
                          help='Export papers to JSON file')
    fetch_parser.add_argument('--export-csv', type=str, metavar='FILENAME',
                          help='Export papers to CSV file')

    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', 
                                         help='Analyze papers for practical AI applications')
    analyze_parser.add_argument('--input', type=str, required=True,
                              help='Input JSON file containing papers')
    analyze_parser.add_argument('--output', type=str, required=True,
                              help='Output JSON file for analyzed papers')
    analyze_parser.add_argument('--min-relevance', type=float, default=0.7,
                              help='Minimum relevance score (0-1)')

    args = parser.parse_args()

    if args.command == 'fetch':
        run_fetcher(args.days, args.export_json, args.export_csv)
    elif args.command == 'analyze':
        run_analyzer(args.input, args.output, args.min_relevance)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()