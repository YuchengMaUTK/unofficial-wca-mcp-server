"""Reference data models (continents, countries, events)."""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field

from .base import PaginatedResponse


class EventFormat(str, Enum):
    """WCA event format types."""
    
    TIME = "time"
    NUMBER = "number" 
    MULTI = "multi"


class Continent(BaseModel):
    """WCA continent information."""
    
    id: str = Field(..., description="Continent identifier", examples=["europe", "asia"])
    name: str = Field(..., description="Continent name", examples=["Europe", "Asia"])


class Country(BaseModel):
    """WCA country information."""
    
    iso2_code: str = Field(..., alias="iso2Code", description="ISO 2-letter country code", examples=["US", "GB"])
    name: str = Field(..., description="Country name", examples=["United States", "United Kingdom"])


class Event(BaseModel):
    """WCA event information."""
    
    id: str = Field(..., description="Event identifier", examples=["333", "222", "444"])
    name: str = Field(..., description="Event name", examples=["3x3x3 Cube", "2x2x2 Cube"])
    format: EventFormat = Field(..., description="Event format type")


# Paginated response types
class Continents(PaginatedResponse[Continent]):
    """Paginated list of continents."""
    pass


class Countries(PaginatedResponse[Country]):
    """Paginated list of countries."""
    pass


class Events(PaginatedResponse[Event]):
    """Paginated list of events."""
    pass