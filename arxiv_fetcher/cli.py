"""Command line interface for the ArXiv paper fetcher."""

import sys
import argparse
from typing import Optional
from datetime import datetime

from .config import (CACHE_FILE, CACHE_DURATION, MAX_RESULTS, 
                          ARXIV_CATEGORIES)
from .cache_manager import CacheManager
from .arxiv_client import ArxivClient
from .formatter import PaperFormatter
from .exporters import export_to_json, export_to_csv
from .paper_analyzer import analyze_papers
from .paper_downloader import PaperDownloader
from .paper_summarizer import PaperSummarizer


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

def run_downloader(input_file: str, output_dir: str) -> None:
    """Run the paper downloader on the analyzed papers."""
    try:
        downloader = PaperDownloader(output_dir)
        downloader.download_papers(input_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def run_parser(titles: Optional[list] = None, date: Optional[str] = None) -> None:
    """Run the paper parser on downloaded papers."""
    from .paper_parser import run_parser
    try:
        run_parser(titles=titles, date=date)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def run_summarizer(titles: Optional[list] = None, date: Optional[str] = None) -> None:
    """Run the paper summarizer with specified titles or date."""
    try:
        summarizer = PaperSummarizer()
        summarizer.process_papers(titles=titles, date=date)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def display_categories() -> None:
    """Display all available arXiv categories."""
    formatter = PaperFormatter()
    formatter.display_categories(ARXIV_CATEGORIES)

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

    # Download command
    download_parser = subparsers.add_parser('download',
                                          help='Download PDFs of analyzed papers')
    download_parser.add_argument('--input', type=str, required=True,
                               help='Input JSON file containing analyzed papers')
    download_parser.add_argument('--output-dir', type=str, default='papers',
                               help='Output directory for downloaded papers')

    # Parse command
    parse_parser = subparsers.add_parser('parse',
                                        help='Parse downloaded papers using LlamaParse')
    group = parse_parser.add_mutually_exclusive_group()
    group.add_argument('--titles', nargs='+', help='Paper titles (folder names) to parse')
    group.add_argument('--date', help='Parse papers downloaded on specific date (YYYY-MM-DD)')

    # Summarize command
    summarize_parser = subparsers.add_parser('summarize', help='Summarize parsed papers using OpenAI')
    summarize_group = summarize_parser.add_mutually_exclusive_group()
    summarize_group.add_argument('--titles', nargs='+', help='Paper titles (folder names) to summarize')
    summarize_group.add_argument('--date', help='Summarize papers downloaded on a specific date (YYYY-MM-DD)')

    # Categories command
    subparsers.add_parser('categories', help='List all available arXiv categories')

    args = parser.parse_args()

    if args.command == 'fetch':
        run_fetcher(args.days, args.export_json, args.export_csv)
    elif args.command == 'analyze':
        run_analyzer(args.input, args.output, args.min_relevance)
    elif args.command == 'download':
        run_downloader(args.input, args.output_dir)
    elif args.command == 'parse':
        run_parser(args.titles, args.date)
    elif args.command == 'summarize':
        run_summarizer(args.titles, args.date)
    elif args.command == 'categories':
        display_categories()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()