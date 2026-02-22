from typing import Dict, List

FEEDS: Dict[str, str] = {
    "openai": "https://status.openai.com/feed.rss"
}

CACHE_HEADERS = {}
SEEN_ENTRIES = set()
INCIDENTS: List[dict] = []