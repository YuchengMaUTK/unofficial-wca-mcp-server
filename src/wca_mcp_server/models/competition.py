"""Competition and championship models."""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field

from .base import PaginatedResponse, Coordinates, ContactInfo


class CompetitionDate(BaseModel):
    """Competition date information."""
    
    from_date: date = Field(..., alias="from", description="Competition start date")
    till: date = Field(..., description="Competition end date")
    number_of_days: int = Field(..., alias="numberOfDays", description="Number of competition days")


class Venue(BaseModel):
    """Competition venue information."""
    
    name: str = Field(..., description="Venue name")
    address: str = Field(..., description="Venue address")
    details: Optional[str] = Field(None, description="Additional venue details")
    coordinates: Optional[Coordinates] = Field(None, description="Venue coordinates")


class Competition(BaseModel):
    """WCA competition information."""
    
    id: str = Field(..., description="Competition identifier")
    name: str = Field(..., description="Competition name")
    city: str = Field(..., description="Competition city")
    country: str = Field(..., description="Competition country code")
    date: CompetitionDate = Field(..., description="Competition date information")
    is_canceled: bool = Field(..., alias="isCanceled", description="Whether competition is canceled")
    events: List[str] = Field(..., description="List of event IDs in the competition")
    wca_delegates: List[ContactInfo] = Field(..., alias="wcaDelegates", description="WCA delegates")
    organisers: List[ContactInfo] = Field(..., description="Competition organizers")
    venue: Venue = Field(..., description="Venue information")
    information: Optional[str] = Field(None, description="Additional competition information")
    external_website: Optional[str] = Field(None, alias="externalWebsite", description="External website URL")


class Championship(Competition):
    """WCA championship information (extends Competition)."""
    
    region: str = Field(..., description="Championship region (world, continent, or country)")


# Paginated response types
class Competitions(PaginatedResponse[Competition]):
    """Paginated list of competitions."""
    pass


class Championships(PaginatedResponse[Championship]):
    """Paginated list of championships."""
    pass