"""Competition result models."""

from typing import List
from pydantic import BaseModel, Field

from .base import PaginatedResponse


class Result(BaseModel):
    """Individual competition result."""
    
    competition_id: str = Field(..., alias="competitionId", description="Competition identifier")
    person_id: str = Field(..., alias="personId", description="WCA ID of the competitor")
    round: str = Field(..., description="Round name")
    position: int = Field(..., description="Final position in the round")
    best: int = Field(..., description="Best single time in centiseconds")
    average: int = Field(..., description="Average time in centiseconds")
    format: str = Field(..., description="Competition format")
    solves: List[int] = Field(..., description="Individual solve times in centiseconds")


# Paginated response types
class Results(PaginatedResponse[Result]):
    """Paginated list of results."""
    pass