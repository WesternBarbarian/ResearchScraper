# ArXiv Fetcher CLI

A command-line tool for fetching and analyzing recent Computer Science and Artificial Intelligence publications from arXiv. Perfect for researchers and developers who want to stay updated with the latest academic papers.

## Features

- Fetch recent papers (1-30 days window)
- Export results to JSON or CSV formats
- Smart caching to prevent redundant API calls
- Rich terminal output formatting
- Focus on CS/AI papers with customizable categories
- Programmatic usage support

## Installation

```bash
# Install from the current directory
pip install .

# The command `arxiv-fetch` will be available after installation
```

## Command-Line Usage

### Basic Usage

```bash
# Fetch papers from the last 7 days (default)
arxiv-fetch

# Fetch papers from the last N days (1-30)
arxiv-fetch --days 14
```

### Export Options

```bash
# Export results to JSON
arxiv-fetch --export-json papers.json

# Export results to CSV
arxiv-fetch --export-csv papers.csv

# Combine multiple options
arxiv-fetch --days 10 --export-json recent.json --export-csv recent.csv
```

## Output Format

When displaying in terminal:
- Paper title
- Authors
- Publication date
- arXiv categories
- Summary (truncated for readability)

## Programmatic Usage

You can use the fetcher in your Python scripts:

```python
from arxiv_fetcher.cli import run_fetcher

# Fetch and display papers
run_fetcher(days=7)

# Fetch and export papers
run_fetcher(days=7, export_json='papers.json', export_csv='papers.csv')
```

## Configuration

The tool uses the following default settings (configurable in `config.py`):
- API request delay: 3 seconds
- Maximum results: 100 papers
- Cache duration: 1 hour
- Default categories: CS and HCI papers

## Cache Behavior

- Results are cached for 1 hour by default
- Cache is stored in `.arxiv_cache.json`
- Cache keys include date to ensure fresh results daily
- Cache is automatically invalidated after expiration

## Error Handling

- Input validation for days (must be 1-30)
- Graceful API error handling
- Clear error messages
- Automatic retry on temporary failures

## Requirements

- Python 3.11 or higher
- Required packages (automatically installed):
  - `arxiv`: For API access
  - `rich`: For formatted terminal output

## Exit Codes

- 0: Success
- 1: Error (with error message displayed)

## Examples

1. Get today's papers:
```bash
arxiv-fetch --days 1
```

2. Export last week's papers:
```bash
arxiv-fetch --days 7 --export-json weekly.json
```

3. Quick look at recent papers:
```bash
arxiv-fetch
```

## Notes

- The tool respects arXiv's API rate limits
- Large requests may take longer due to API throttling
- Cache helps reduce API load and speeds up repeated queries