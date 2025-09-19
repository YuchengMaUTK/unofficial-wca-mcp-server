"""Data models for the WCA MCP Server."""

# Base models
from .base import Pagination, PaginatedResponse, Coordinates, ContactInfo, RankInfo

# Reference data models
from .reference import EventFormat, Continent, Country, Event, Continents, Countries, Events

# Competition models
from .competition import CompetitionDate, Venue, Competition, Championship, Competitions, Championships

# Person models
from .person import (
    EventRank, MedalCount, RecordType, Records, PersonRanks, 
    CompetitionResult, Person, Persons
)

# Ranking models
from .ranking import RankType, Rank, Ranks

# Result models
from .result import Result, Results

# Request models
from .requests import (
    PersonDetailsRequest,
    RankingRequest, CompetitionDetailsRequest, CompetitionResultsRequest,
    ChampionshipSearchRequest, ChampionshipDetailsRequest
)

__all__ = [
    # Base models
    "Pagination", "PaginatedResponse", "Coordinates", "ContactInfo", "RankInfo",
    
    # Reference data models
    "EventFormat", "Continent", "Country", "Event", "Continents", "Countries", "Events",
    
    # Competition models
    "CompetitionDate", "Venue", "Competition", "Championship", "Competitions", "Championships",
    
    # Person models
    "EventRank", "MedalCount", "RecordType", "Records", "PersonRanks", 
    "CompetitionResult", "Person", "Persons",
    
    # Ranking models
    "RankType", "Rank", "Ranks",
    
    # Result models
    "Result", "Results",
    
    # Request models
    "PersonDetailsRequest",
    "RankingRequest", "CompetitionDetailsRequest", "CompetitionResultsRequest",
    "ChampionshipSearchRequest", "ChampionshipDetailsRequest",
]