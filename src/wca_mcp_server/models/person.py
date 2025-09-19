"""Person and competitor models."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from .base import PaginatedResponse, RankInfo


class EventRank(BaseModel):
    """Ranking information for a specific event."""
    
    event_id: str = Field(..., alias="eventId", description="Event identifier")
    best: int = Field(..., description="Best time/score in centiseconds or points")
    rank: RankInfo = Field(..., description="Ranking positions")


class MedalCount(BaseModel):
    """Medal count information."""
    
    gold: int = Field(..., description="Number of gold medals")
    silver: int = Field(..., description="Number of silver medals") 
    bronze: int = Field(..., description="Number of bronze medals")


class RecordType(BaseModel):
    """Record count by type."""
    
    wr: int = Field(..., alias="WR", description="World Records")
    cr: int = Field(..., alias="CR", description="Continental Records")
    nr: int = Field(..., alias="NR", description="National Records")


class Records(BaseModel):
    """Record information for singles and averages."""
    
    single: RecordType = Field(..., description="Single solve records")
    average: RecordType = Field(..., description="Average solve records")


class PersonRanks(BaseModel):
    """Person's ranking information."""
    
    singles: List[EventRank] = Field(..., description="Single solve rankings")
    averages: List[EventRank] = Field(..., description="Average solve rankings")


class CompetitionResult(BaseModel):
    """Result for a specific round in a competition."""
    
    round: str = Field(..., description="Round name")
    position: int = Field(..., description="Final position in round")
    best: int = Field(..., description="Best single time in centiseconds")
    average: int = Field(..., description="Average time in centiseconds")
    format: str = Field(..., description="Competition format")
    solves: List[int] = Field(..., description="Individual solve times in centiseconds")


class Person(BaseModel):
    """WCA person/competitor information."""
    
    id: str = Field(..., description="WCA ID")
    name: str = Field(..., description="Full name")
    slug: str = Field(..., description="URL slug")
    country: str = Field(..., description="Country code")
    number_of_competitions: int = Field(..., alias="numberOfCompetitions", description="Total competitions attended")
    competition_ids: List[str] = Field(..., alias="competitionIds", description="List of competition IDs")
    number_of_championships: int = Field(..., alias="numberOfChampionships", description="Total championships attended")
    championship_ids: List[str] = Field(..., alias="championshipIds", description="List of championship IDs")
    rank: PersonRanks = Field(..., description="Ranking information")
    medals: MedalCount = Field(..., description="Medal counts")
    records: Records = Field(..., description="Record counts")
    results: Dict[str, Dict[str, List[CompetitionResult]]] = Field(
        ..., 
        description="Competition results organized by competition ID and event ID"
    )


# Paginated response types
class Persons(PaginatedResponse[Person]):
    """Paginated list of persons."""
    pass