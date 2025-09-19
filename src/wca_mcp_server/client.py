"""WCA API client implementation."""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlencode

import httpx
from pydantic import ValidationError

from .config import get_settings
from .models.base import APIError, PaginatedResponse


logger = logging.getLogger(__name__)


class WCAAPIClient:
    """Async HTTP client for the WCA API."""
    
    def __init__(self, base_url: Optional[str] = None, timeout: float = 30.0):
        """Initialize the WCA API client.
        
        Args:
            base_url: Base URL for the WCA API. Defaults to settings.
            timeout: Request timeout in seconds.
        """
        settings = get_settings()
        self.base_url = base_url or settings.api_base_url
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        await self._ensure_client()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None
            
    async def _ensure_client(self) -> None:
        """Ensure HTTP client is initialized."""
        if not self._client:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(self.timeout),
                limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
                headers={
                    "User-Agent": "WCA-MCP-Server/1.0.0",
                    "Accept": "application/json",
                }
            )
    
    async def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        retries: int = 3
    ) -> Dict[str, Any]:
        """Make an HTTP request to the WCA API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            retries: Number of retry attempts
            
        Returns:
            JSON response data
            
        Raises:
            APIError: If the request fails after retries
        """
        await self._ensure_client()
        
        # Ensure proper URL construction for static API
        if self.base_url.endswith('/'):
            url = self.base_url + endpoint
        else:
            url = self.base_url + '/' + endpoint
        if params:
            # Filter out None values
            params = {k: v for k, v in params.items() if v is not None}
        
        last_exception = None
        
        for attempt in range(retries + 1):
            try:
                logger.debug(f"Making request to {url} with params {params} (attempt {attempt + 1})")
                
                response = await self._client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                logger.debug(f"Request successful, received {len(str(data))} bytes")
                return data
                
            except httpx.HTTPStatusError as e:
                logger.warning(f"HTTP error {e.response.status_code} for {url}: {e}")
                if e.response.status_code == 404:
                    raise APIError(f"Resource not found: {endpoint}", status_code=404)
                elif e.response.status_code >= 500 and attempt < retries:
                    # Retry on server errors
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    raise APIError(f"HTTP {e.response.status_code}: {e}", status_code=e.response.status_code)
                    
            except (httpx.RequestError, httpx.TimeoutException) as e:
                logger.warning(f"Request error for {url}: {e}")
                last_exception = e
                if attempt < retries:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                    
            except Exception as e:
                logger.error(f"Unexpected error for {url}: {e}")
                raise APIError(f"Unexpected error: {e}")
        
        # If we get here, all retries failed
        raise APIError(f"Request failed after {retries + 1} attempts: {last_exception}")
    

    async def get_competition(self, competition_id: str) -> Dict[str, Any]:
        """Get a specific competition by ID.
        
        Args:
            competition_id: Competition ID
            
        Returns:
            Competition data
        """
        return await self._make_request(f"competitions/{competition_id}.json")
    
    async def get_competitions_by_date(
        self,
        year: int,
        month: int,
        day: int
    ) -> Dict[str, Any]:
        """Get competitions on a specific date.
        
        Args:
            year: Year (e.g., 2023, 2024)
            month: Month (1-12)
            day: Day (1-31)
            
        Returns:
            Competition data for the specific date
        """
        month_str = f"{month:02d}"  # Ensure 2-digit format
        day_str = f"{day:02d}"      # Ensure 2-digit format
        endpoint = f"competitions/{year}/{month_str}/{day_str}.json"
        return await self._make_request(endpoint)
    
    async def get_competitions_by_event(
        self,
        event_id: str,
        page: int = 1
    ) -> Dict[str, Any]:
        """Get competitions that feature a specific event.
        
        Args:
            event_id: Event ID (e.g., "333", "222", "333bf")
            page: Page number (1-based)
            
        Returns:
            Paginated competition data for the event
        """
        if page == 1:
            endpoint = f"competitions/{event_id}.json"
        else:
            endpoint = f"competitions/{event_id}-page-{page}.json"
        return await self._make_request(endpoint)
    

    async def get_person(self, wca_id: str) -> Dict[str, Any]:
        """Get a specific person by WCA ID.
        
        Args:
            wca_id: WCA ID (e.g., "2003SEAR02")
            
        Returns:
            Person data
        """
        return await self._make_request(f"persons/{wca_id}.json")
    
    async def get_rankings(
        self,
        event_id: str,
        region: str = "world",
        type: str = "single",
        page: int = 1,
        per_page: int = 25
    ) -> Dict[str, Any]:
        """Get rankings for an event.
        
        Args:
            event_id: Event ID (e.g., "333")
            region: Region code ("world", continent code, or country ISO2)
            type: Ranking type ("single" or "average")
            page: Page number (1-based)
            per_page: Items per page (max 100)
            
        Returns:
            Paginated ranking data
        """
        # The static API uses a specific URL format: rank/{region}/{type}/{event}.json
        return await self._make_request(f"rank/{region}/{type}/{event_id}.json")
    
    async def get_competition_results(
        self,
        competition_id: str
    ) -> Dict[str, Any]:
        """Get all results for a competition.
        
        Args:
            competition_id: Competition ID
            
        Returns:
            All result data for the competition
        """
        return await self._make_request(f"results/{competition_id}.json")
    
    async def get_competition_event_results(
        self,
        competition_id: str,
        event_id: str
    ) -> Dict[str, Any]:
        """Get results for a specific event in a competition.
        
        Args:
            competition_id: Competition ID
            event_id: Event ID (e.g., "333", "222")
            
        Returns:
            Result data for the specific event in the competition
        """
        return await self._make_request(f"results/{competition_id}/{event_id}.json")
    
    async def get_championships(
        self,
        page: int = 1,
        per_page: int = 25,
        **filters
    ) -> Dict[str, Any]:
        """Get championships with optional filtering.
        
        Args:
            page: Page number (1-based) - Note: static API doesn't support pagination
            per_page: Items per page (max 100) - Note: static API doesn't support pagination
            **filters: Additional filter parameters - Note: static API has limited filtering
            
        Returns:
            Paginated championship data
        """
        # For the static API, we get all championships and handle filtering/pagination client-side
        data = await self._make_request("championships.json")
        
        # Handle filtering by type if specified
        items = data.get("items", []) if isinstance(data, dict) else []
        
        if "type" in filters:
            filter_type = filters["type"].lower()
            if filter_type == "world":
                items = [item for item in items if item.get("region") == "world"]
            else:
                # Filter by region (continent or country)
                items = [item for item in items if item.get("region", "").lower() == filter_type]
        
        # Simple client-side pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_items = items[start_idx:end_idx]
        
        return {
            "items": paginated_items,
            "total": len(items),
            "page": page,
            "per_page": per_page,
            "pagination": {
                "page": page,
                "size": per_page,
                "total_pages": (len(items) + per_page - 1) // per_page
            }
        }
    
    async def get_championship(self, championship_id: str) -> Dict[str, Any]:
        """Get a specific championship by ID.
        
        Args:
            championship_id: Championship ID
            
        Returns:
            Championship data
        """
        return await self._make_request(f"championships/{championship_id}.json")
    
    async def get_events(self) -> List[Dict[str, Any]]:
        """Get all WCA events.
        
        Returns:
            List of event data
        """
        data = await self._make_request("events.json")
        # The API returns paginated data with items array
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        # Fallback for other formats
        if isinstance(data, list):
            return data
        return data.get("events", [])
    
    async def get_countries(self) -> List[Dict[str, Any]]:
        """Get all countries.
        
        Returns:
            List of country data
        """
        data = await self._make_request("countries.json")
        # The API returns paginated data with items array
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        return data.get("countries", [])
    
    async def get_continents(self) -> List[Dict[str, Any]]:
        """Get all continents.
        
        Returns:
            List of continent data
        """
        data = await self._make_request("continents.json")
        # The API returns paginated data with items array
        if isinstance(data, dict) and "items" in data:
            return data["items"]
        return data.get("continents", [])