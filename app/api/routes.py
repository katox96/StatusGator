from fastapi import APIRouter, HTTPException
from datetime import datetime, date
from typing import Optional

from ..store import INCIDENTS, FEEDS
from ..models import FeedIn

router = APIRouter()


@router.get("/incidents")
def get_incidents(
    incident_date: Optional[date] = None,
    feed: Optional[str] = None
):
    target_date = incident_date or datetime.utcnow().date()

    result = [
        i for i in INCIDENTS
        if i["date"] == target_date
        and (feed is None or i["feed"] == feed)
    ]

    return {"count": len(result), "data": result}


@router.post("/feeds")
def add_feed(feed: FeedIn):
    if feed.name in FEEDS:
        raise HTTPException(400, "Feed already exists")

    FEEDS[feed.name] = feed.url
    return {"message": "Feed added", "feeds": FEEDS}