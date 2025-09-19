"""Request models for tool parameters and validation."""

from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator





class PersonDetailsRequest(BaseModel):
    """Request parameters for person details."""
    
    person_id: str = Field(..., description="WCA ID of the person")


class RankingRequest(BaseModel):
    """Request parameters for rankings."""
    
    region: str = Field(..., description="Region (world, continent code, or country code)")
    rank_type: Literal["single", "average"] = Field(..., description="Type of ranking")
    event: str = Field(..., description="Event ID")
    
    @field_validator('region')
    @classmethod
    def validate_region(cls, v):
        return v.lower()


class CompetitionDetailsRequest(BaseModel):
    """Request parameters for competition details."""
    
    competition_id: str = Field(..., description="Competition identifier")


class CompetitionResultsRequest(BaseModel):
    """Request parameters for competition results."""
    
    competition_id: str = Field(..., description="Competition identifier")
    event: Optional[str] = Field(None, description="Event ID (optional)")


class ChampionshipSearchRequest(BaseModel):
    """Request parameters for championship search."""
    
    page: Optional[int] = Field(None, ge=1, description="Page number for pagination")
    championship_type: Optional[str] = Field(None, description="Championship type (world, continent, or country)")


class ChampionshipDetailsRequest(BaseModel):
    """Request parameters for championship details."""
    
    championship_id: str = Field(..., min_length=1, description="Championship identifier")