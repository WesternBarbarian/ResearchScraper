"""Configuration settings for the arXiv papers fetcher."""

# API Settings
ARXIV_API_URL = "http://export.arxiv.org/api/query"
API_DELAY = 3  # seconds between requests
MAX_RESULTS = 100

# Categories of interest
#CS_AI_CATEGORIES = [
#    "cs.AI",    # Artificial Intelligence
#]

#CS_ADDITIONAL_CATEGORIES = [
#    "cs.HC",    # Human-Computer Interaction
#    "cs.CY",    # Computers and Society (includes business applications)
#]

# Query combinations
QUERY_COMBINATIONS = [
    ("cs.CY", "cs.HC"),  # AI + HCI papers
  #  ("cs.AI", "cs.CY"),  # AI + Business/Society papers
]

# Cache settings
CACHE_DURATION = 3600  # 1 hour in seconds
CACHE_FILE = ".arxiv_cache.json"

# Output settings
MAX_ABSTRACT_LENGTH = 500
DATE_FORMAT = "%Y-%m-%d"