import asyncio
from datetime import datetime

import aiohttp
import feedparser

from .store import FEEDS, CACHE_HEADERS, SEEN_ENTRIES, INCIDENTS


def extract_service(title: str) -> str:
    return title.split("]")[-1].strip()


def normalize_date(entry):
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime(*entry.published_parsed[:6]).date()
    return datetime.now().date()


async def fetch_feed(session, name, url):
    headers = {}

    if name in CACHE_HEADERS:
        if CACHE_HEADERS[name].get("etag"):
            headers["If-None-Match"] = CACHE_HEADERS[name]["etag"]
        if CACHE_HEADERS[name].get("modified"):
            headers["If-Modified-Since"] = CACHE_HEADERS[name]["modified"]

    async with session.get(url, headers=headers) as resp:

        if resp.status == 304:
            return

        CACHE_HEADERS[name] = {
            "etag": resp.headers.get("ETag"),
            "modified": resp.headers.get("Last-Modified"),
        }

        text = await resp.text()
        feed = feedparser.parse(text)

        for entry in feed.entries:
            if entry.id not in SEEN_ENTRIES:
                SEEN_ENTRIES.add(entry.id)

                incident = {
                    "feed": name,
                    "service": extract_service(entry.title),
                    "message": entry.title,
                    "link": entry.link,
                    "date": normalize_date(entry),
                }

                INCIDENTS.append(incident)

                # print("\n🚨 NEW STATUS UPDATE")
                # print(incident)


async def watcher():
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [
                fetch_feed(session, name, url)
                for name, url in FEEDS.items()
            ]
            await asyncio.gather(*tasks)
            await asyncio.sleep(60)