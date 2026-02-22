from pydantic import BaseModel
from datetime import date
from typing import Optional


class FeedIn(BaseModel):
    name: str
    url: str


class IncidentQuery(BaseModel):
    incident_date: Optional[date] = None
    feed: Optional[str] = None