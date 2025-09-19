"""Ranking and record models."""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field

from .base import PaginatedResponse, RankInfo


class RankType(str, Enum):
    """Type of ranking (single or average)."""
    
    SINGLE = "single"
    AVERAGE = "average"


class Rank(BaseModel):
    """Individual ranking entry."""
    
    rank_type: RankType = Field(..., alias="rankType", description="Type of ranking")
    person_id: str = Field(..., alias="personId", description="WCA ID of the person")
    event_id: str = Field(..., alias="eventId", description="Event identifier")
    best: int = Field(..., description="Best time/score in centiseconds or points")
    rank: RankInfo = Field(..., description="Ranking positions across regions")


# Paginated response types
class Ranks(PaginatedResponse[Rank]):
    """Paginated list of rankings."""
    pass