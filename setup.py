
from setuptools import setup, find_packages

setup(
    name="arxiv-fetcher",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "arxiv>=2.1.3",
        "llama-index>=0.12.14",
        "llama-parse>=0.5.20",
        "openai>=1.60.1",
        "python-dotenv>=1.0.1",
        "rich>=13.9.4",
    ],
    entry_points={
        "console_scripts": [
            "arxiv-fetch=arxiv_fetcher.cli:main",
        ],
    },
)
