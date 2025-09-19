"""Base models and common structures for the WCA MCP Server."""

from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field


class APIError(Exception):
    """Custom exception for WCA API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        """Initialize API error.
        
        Args:
            message: Error message
            status_code: HTTP status code if applicable
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        
    def __str__(self) -> str:
        if self.status_code:
            return f"API Error {self.status_code}: {self.message}"
        return f"API Error: {self.message}"


class Pagination(BaseModel):
    """Pagination information for API responses."""
    
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of items per page")


T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response structure."""
    
    pagination: Pagination = Field(..., description="Pagination information")
    total: int = Field(..., description="Total number of items available")
    items: List[T] = Field(..., description="List of items for the current page")


class Coordinates(BaseModel):
    """Geographic coordinates."""
    
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")


class ContactInfo(BaseModel):
    """Contact information for delegates and organizers."""
    
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")


class RankInfo(BaseModel):
    """Ranking information across different regions."""
    
    world: int = Field(..., description="World ranking position")
    continent: int = Field(..., description="Continental ranking position") 
    country: int = Field(..., description="National ranking position")