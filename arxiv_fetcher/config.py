"""Configuration settings for the arXiv papers fetcher."""

# API Settings
ARXIV_API_URL = "http://export.arxiv.org/api/query"
API_DELAY = 3  # seconds between requests
MAX_RESULTS = 100

# Query combinations
QUERY_COMBINATIONS = [
    ("cs.CY", "cs.HC"),  # AI + HCI papers
]

# Cache settings
CACHE_DURATION = 3600  # 1 hour in seconds
CACHE_FILE = ".arxiv_cache.json"

# Output settings
MAX_ABSTRACT_LENGTH = 500
DATE_FORMAT = "%Y-%m-%d"
