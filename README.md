# ArXiv Fetcher CLI

A command-line tool for fetching and analyzing recent Computer Science and Artificial Intelligence publications from arXiv. Perfect for researchers and developers who want to stay updated with the latest academic papers.

## Features

- Fetch recent papers (1-30 days window)
- Export results to JSON or CSV formats
- Smart caching to prevent redundant API calls
- Rich terminal output formatting
- Focus on CS/AI papers with customizable categories
- Programmatic usage support
- AI-powered paper analysis for practical applications and thought leadership

## Installation

```bash
# Install from the current directory
pip install .

# The command `arxiv-fetch` will be available after installation
```

## Command-Line Usage

The tool provides two main commands: `fetch` for retrieving papers and `analyze` for identifying relevant papers using AI.

### Basic Usage

```bash
# Fetch papers from the last 7 days (default)
arxiv-fetch fetch

# Fetch papers from the last N days (1-30)
arxiv-fetch fetch --days 14
```

### Export Options

```bash
# Export results to JSON
arxiv-fetch fetch --export-json papers.json

# Export results to CSV
arxiv-fetch fetch --export-csv papers.csv

# Combine multiple options
arxiv-fetch fetch --days 10 --export-json recent.json --export-csv recent.csv
```

### Paper Analysis

The analyzer uses GPT-4o to identify papers relevant to practical AI applications and thought leadership:

```bash
# Analyze papers from a JSON file
arxiv-fetch analyze --input papers.json --output analyzed_papers.json

# Customize minimum relevance score (default: 0.7)
arxiv-fetch analyze --input papers.json --output analyzed_papers.json --min-relevance 0.8
```

The analyzer outputs include:
- Relevance score (0-1)
- Practical applications assessment
- Thought leadership value
- Key insights
- Original paper metadata for retrieval

## Output Format

When displaying in terminal:
- Paper title
- Authors
- Publication date
- arXiv categories
- Summary (truncated for readability)

Analysis output includes:
- All original paper metadata
- AI-generated analysis of practical applications
- Thought leadership assessment
- Relevance scoring
- Key insights extracted from the paper

## Programmatic Usage

You can use the fetcher in your Python scripts:

```python
from arxiv_fetcher.cli import run_fetcher, run_analyzer

# Fetch and display papers
run_fetcher(days=7)

# Fetch and export papers
run_fetcher(days=7, export_json='papers.json', export_csv='papers.csv')

# Analyze papers for practical relevance
run_analyzer(input_file='papers.json', output_file='analyzed_papers.json', min_relevance_score=0.7)
```

## Configuration

The tool uses the following default settings (configurable in `config.py`):
- API request delay: 3 seconds
- Maximum results: 100 papers
- Cache duration: 1 hour
- Default categories: CS and HCI papers
- Minimum relevance score: 0.7 (for analysis)

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
  - `openai`: For paper analysis

## Exit Codes

- 0: Success
- 1: Error (with error message displayed)

## Examples

1. Get today's papers:
```bash
arxiv-fetch fetch --days 1
```

2. Export last week's papers:
```bash
arxiv-fetch fetch --days 7 --export-json weekly.json
```

3. Quick look at recent papers:
```bash
arxiv-fetch fetch
```

4. Analyze papers for practical relevance:
```bash
arxiv-fetch analyze --input papers.json --output analyzed_papers.json
```

## Notes

- The tool respects arXiv's API rate limits
- Large requests may take longer due to API throttling
- Cache helps reduce API load and speeds up repeated queries
- Analysis requires an OpenAI API key in the environment