"""Main MCP server implementation for the WCA MCP Server."""

import logging
from typing import List, Dict, Any
from fastmcp import FastMCP
from .config import get_settings
from .client import WCAAPIClient
from .models.base import APIError


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# Initialize settings and logging
settings = get_settings()
setup_logging(settings.log_level)

# Create the FastMCP server instance
mcp = FastMCP("WCA MCP Server")


@mcp.tool()
async def get_wca_events() -> List[Dict[str, Any]]:
    """Get all official WCA events.
    
    Returns a list of all official World Cube Association events including
    event IDs, names, and formats.
    
    Returns:
        List of WCA events with their details
    """
    try:
        async with WCAAPIClient() as client:
            events = await client.get_events()
            return events
    except APIError as e:
        raise Exception(f"Failed to fetch WCA events: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error fetching WCA events: {e}")


@mcp.tool()
async def get_wca_countries() -> List[Dict[str, Any]]:
    """Get all WCA countries.
    
    Returns a list of all countries recognized by the World Cube Association
    including country names and ISO2 codes used for regional filtering.
    
    Returns:
        List of WCA countries with names and ISO2 codes
    """
    try:
        async with WCAAPIClient() as client:
            countries = await client.get_countries()
            return countries
    except APIError as e:
        raise Exception(f"Failed to fetch WCA countries: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error fetching WCA countries: {e}")


@mcp.tool()
async def get_wca_continents() -> List[Dict[str, Any]]:
    """Get all WCA continents.
    
    Returns a list of all continents recognized by the World Cube Association
    including continent names and identifiers used for regional filtering.
    
    Returns:
        List of WCA continents with names and identifiers
    """
    try:
        async with WCAAPIClient() as client:
            continents = await client.get_continents()
            return continents
    except APIError as e:
        raise Exception(f"Failed to fetch WCA continents: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error fetching WCA continents: {e}")


@mcp.tool()
async def get_person_by_wca_id(
    wca_id: str,
    competition_id: str = None,
    include_competition_results: bool = False,
    include_personal_records: bool = True,
    include_rankings: bool = True,
    include_medals: bool = True,
    max_recent_competitions: int = 5
) -> Dict[str, Any]:
    """Get detailed information about a specific WCA competitor by their WCA ID.
    
    Returns information about a speedcuber with configurable detail levels.
    By default, returns basic info, personal records, rankings, and medals without
    the verbose competition results that can make responses extremely long.
    
    Args:
        wca_id: WCA ID of the person (e.g., "2003SEAR02")
        competition_id: Optional competition ID to get results from a specific competition (e.g., "WC2023")
        include_competition_results: Include detailed competition results (default: False)
        include_personal_records: Include personal best records (default: True)
        include_rankings: Include current world/continental/national rankings (default: True)
        include_medals: Include medal counts (default: True)
        max_recent_competitions: If including results, limit to N most recent competitions (default: 5)
        
    Returns:
        Filtered person information based on the specified parameters
    """
    try:
        async with WCAAPIClient() as client:
            person_data = await client.get_person(wca_id)
            
            # Create filtered response
            filtered_data = {
                "id": person_data.get("id"),
                "name": person_data.get("name"),
                "slug": person_data.get("slug"),
                "country": person_data.get("country"),
                "numberOfCompetitions": person_data.get("numberOfCompetitions"),
                "numberOfChampionships": person_data.get("numberOfChampionships"),
            }
            
            # Add competition IDs list (always include as it's lightweight)
            if "competitionIds" in person_data:
                filtered_data["competitionIds"] = person_data["competitionIds"]
            if "championshipIds" in person_data:
                filtered_data["championshipIds"] = person_data["championshipIds"]
            
            # Add personal records if requested
            if include_personal_records and "records" in person_data:
                filtered_data["records"] = person_data["records"]
            
            # Add rankings if requested
            if include_rankings and "rank" in person_data:
                filtered_data["rank"] = person_data["rank"]
            
            # Add medals if requested
            if include_medals and "medals" in person_data:
                filtered_data["medals"] = person_data["medals"]
            
            # Handle specific competition results if competition_id is provided
            if competition_id:
                competition_ids = person_data.get("competitionIds", [])
                results = person_data.get("results", {})
                
                if competition_id in competition_ids:
                    # Person participated in this competition
                    if competition_id in results:
                        # Results data is available
                        filtered_data["results"] = {competition_id: results[competition_id]}
                        filtered_data["_results_note"] = f"Showing results from competition: {competition_id}"
                    else:
                        # Person participated but no results data available
                        filtered_data["results"] = {}
                        filtered_data["_results_note"] = f"Person participated in {competition_id} but no results data available"
                else:
                    # Person did not participate in this competition
                    filtered_data["results"] = {}
                    filtered_data["_results_note"] = f"Person did not participate in competition: {competition_id}"
            
            # Add competition results if requested (with optional limiting)
            elif include_competition_results and "results" in person_data:
                results = person_data["results"]
                if max_recent_competitions and max_recent_competitions > 0:
                    # Get the most recent competitions (competition IDs are typically in chronological order)
                    competition_ids = person_data.get("competitionIds", [])
                    recent_competition_ids = competition_ids[-max_recent_competitions:] if competition_ids else []
                    
                    # Filter results to only include recent competitions
                    filtered_results = {
                        comp_id: results[comp_id] 
                        for comp_id in recent_competition_ids 
                        if comp_id in results
                    }
                    filtered_data["results"] = filtered_results
                    filtered_data["_results_note"] = f"Showing results from {len(filtered_results)} most recent competitions out of {len(results)} total"
                else:
                    filtered_data["results"] = results
            elif not include_competition_results and not competition_id:
                # Explicitly exclude results when not requested
                filtered_data["_results_note"] = f"Competition results excluded (set include_competition_results=True to include). Total competitions: {person_data.get('numberOfCompetitions', 0)}"
            
            return filtered_data
            
    except APIError as e:
        raise Exception(f"Failed to get person {wca_id}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error getting person {wca_id}: {e}")


@mcp.tool()
async def get_rankings(
    event_id: str,
    region: str = "world",
    ranking_type: str = "single",
    page: int = 1,
    per_page: int = 25
) -> Dict[str, Any]:
    """Get current world rankings and records for a specific event.
    
    Returns the current rankings for any WCA event, which includes world records
    and top performers. Can filter by region (world, continent, or country).
    
    Args:
        event_id: WCA event ID (e.g., "333" for 3x3x3 Cube, "222" for 2x2x2)
        region: Region code - "world" for world rankings, continent codes like "Europe", 
                or country ISO2 codes like "US", "CN" (default: "world")
        ranking_type: Type of ranking - "single" for single solve records or 
                     "average" for average records (default: "single")
        page: Page number (1-based, default: 1)
        per_page: Items per page (max 100, default: 25)
        
    Returns:
        Paginated ranking data with current records and top performers
    """
    try:
        async with WCAAPIClient() as client:
            rankings_data = await client.get_rankings(
                event_id=event_id,
                region=region,
                type=ranking_type,
                page=page,
                per_page=per_page
            )
            return rankings_data
    except APIError as e:
        raise Exception(f"Failed to get rankings for {event_id}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error getting rankings for {event_id}: {e}")




@mcp.tool()
async def search_competitions_by_date(
    year: int,
    month: int,
    day: int
) -> Dict[str, Any]:
    """Search for WCA competitions on a specific date.
    
    Returns a small, focused list of competitions that occurred on the exact date specified.
    This typically returns 1-5 competitions, making it perfect for LLM processing.
    
    Args:
        year: Year (e.g., 2023, 2024)
        month: Month (1-12)
        day: Day (1-31)
        
    Returns:
        Competition data for the specific date (typically 1-5 competitions)
        
    Example:
        search_competitions_by_date(year=2024, month=3, day=15) - Competitions on March 15, 2024
    """
    try:
        async with WCAAPIClient() as client:
            competitions_data = await client.get_competitions_by_date(year, month, day)
            return competitions_data
    except APIError as e:
        raise Exception(f"Failed to search competitions by date: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error searching competitions by date: {e}")


@mcp.tool()
async def search_competitions_by_event(
    event_id: str,
    page: int = 1
) -> Dict[str, Any]:
    """Search for WCA competitions that include a specific event.
    
    Returns competitions that feature the specified WCA event. Results are paginated
    to manage the response size.
    
    Args:
        event_id: WCA event ID (e.g., "333" for 3x3x3 Cube, "222" for 2x2x2, "333bf" for 3x3x3 Blindfolded)
        page: Page number for pagination (default: 1)
        
    Returns:
        Paginated competition data for competitions featuring the specified event
        
    Example:
        search_competitions_by_event(event_id="333bf") - Competitions with 3x3x3 Blindfolded
    """
    try:
        async with WCAAPIClient() as client:
            competitions_data = await client.get_competitions_by_event(event_id, page)
            return competitions_data
    except APIError as e:
        raise Exception(f"Failed to search competitions by event: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error searching competitions by event: {e}")


@mcp.tool()
async def get_competition_by_id(competition_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific competition by its ID.
    
    Returns comprehensive information about a WCA competition including
    venue details, events, results, and organizer information.
    
    Args:
        competition_id: WCA competition ID (e.g., "WC2023")
        
    Returns:
        Detailed competition information
    """
    try:
        async with WCAAPIClient() as client:
            competition_data = await client.get_competition(competition_id)
            return competition_data
    except APIError as e:
        raise Exception(f"Failed to get competition {competition_id}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error getting competition {competition_id}: {e}")


@mcp.tool()
async def search_championships(
    page: int = 1,
    championship_type: str = None
) -> Dict[str, Any]:
    """Search for WCA championships with optional filtering.
    
    Returns championship competitions which are the most prestigious competitions
    in speedcubing including World Championships, Continental Championships, and
    National Championships.
    
    Args:
        page: Page number for pagination (default: 1)
        championship_type: Filter by championship type:
                          - "world" for World Championships
                          - continent codes like "Europe", "Asia", "North America" for Continental Championships  
                          - country ISO2 codes like "US", "CN", "DE" for National Championships
                          - None for all championships (default)
        
    Returns:
        Paginated championship data with competition details
        
    Example:
        search_championships(championship_type="world") - World Championships only
        search_championships(championship_type="US") - US National Championships
    """
    try:
        async with WCAAPIClient() as client:
            # Build filters based on championship_type
            filters = {}
            if championship_type:
                # The API expects the type parameter for filtering
                filters["type"] = championship_type.lower()
            
            championships_data = await client.get_championships(
                page=page,
                **filters
            )
            return championships_data
    except APIError as e:
        raise Exception(f"Failed to search championships: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error searching championships: {e}")


@mcp.tool()
async def get_championship_details(championship_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific championship by its ID.
    
    Returns comprehensive information about a WCA championship including
    venue details, events, results, competitors, and championship-specific
    information like regional significance.
    
    Args:
        championship_id: Championship ID (e.g., "WC2023" for World Championship 2023,
                        "Euro2022" for European Championship 2022)
        
    Returns:
        Detailed championship information including all competition data
        plus championship-specific details
        
    Example:
        get_championship_details("WC2023") - World Championship 2023 details
    """
    try:
        async with WCAAPIClient() as client:
            championship_data = await client.get_championship(championship_id)
            return championship_data
    except APIError as e:
        raise Exception(f"Failed to get championship {championship_id}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error getting championship {championship_id}: {e}")


@mcp.tool()
async def get_competition_results(competition_id: str) -> Dict[str, Any]:
    """Get all results for a WCA competition.
    
    Returns comprehensive results data for all events in a competition,
    including competitor performances, solve breakdowns, round information,
    and final rankings. This provides complete competition outcome data.
    
    Args:
        competition_id: WCA competition ID (e.g., "WC2023", "CubingUSANationals2024")
        
    Returns:
        Complete results data for all events in the competition including:
        - Individual solve times and averages
        - Round-by-round progression
        - Final rankings and positions
        - DNF/DNS information
        - Competitor details
        
    Example:
        get_competition_results("WC2023") - All results from World Championship 2023
    """
    try:
        async with WCAAPIClient() as client:
            results_data = await client.get_competition_results(competition_id)
            return results_data
    except APIError as e:
        raise Exception(f"Failed to get results for competition {competition_id}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error getting results for competition {competition_id}: {e}")


@mcp.tool()
async def get_competition_event_results(
    competition_id: str,
    event_id: str,
    round: str = "Final",
    limit: int = None,
    include_solves: bool = False
) -> Dict[str, Any]:
    """Get results for a specific event within a WCA competition.
    
    Returns focused results data for a single event in a competition.
    By default, returns only Final round results for better LLM processing.
    
    Args:
        competition_id: WCA competition ID (e.g., "WC2025", "CubingUSANationals2024")
        event_id: WCA event ID (e.g., "333" for 3x3x3 Cube, "222" for 2x2x2, 
                 "333bf" for 3x3x3 Blindfolded, "444" for 4x4x4)
        round: Specific round to filter by (default: "Final"). 
               Use "all" for all rounds, or specify: "Final", "Semi Final", 
               "Second round", "First round"
        limit: Maximum number of results to return (optional)
        include_solves: Whether to include detailed solve times (default: False)
        
    Returns:
        Filtered results data including:
        - Competitor performances for the specified round
        - Position, best single, and average times
        - Optionally detailed solve breakdowns
        
    Example:
        get_competition_event_results("WC2025", "333") - Final round only (16 results)
        get_competition_event_results("WC2025", "333", round="all") - All rounds (2490 results)
        get_competition_event_results("WC2025", "333", limit=10) - Top 10 from Final
    """
    try:
        async with WCAAPIClient() as client:
            # Get all results first
            all_results = await client.get_competition_event_results(competition_id, event_id)
            
            if not all_results or 'items' not in all_results:
                return all_results
            
            items = all_results['items']
            
            # Filter by round if specified
            if round != "all":
                items = [item for item in items if item.get('round') == round]
            
            # Apply limit if specified
            if limit:
                items = items[:limit]
            
            # Clean up data for LLM consumption
            cleaned_items = []
            for item in items:
                cleaned_item = {
                    'personId': item.get('personId'),
                    'round': item.get('round'),
                    'position': item.get('position'),
                    'best': item.get('best'),
                    'average': item.get('average')
                }
                
                # Include solves only if requested
                if include_solves:
                    cleaned_item['solves'] = item.get('solves', [])
                
                cleaned_items.append(cleaned_item)
            
            # Return filtered and cleaned results
            return {
                'pagination': {
                    'page': 1,
                    'size': len(cleaned_items)
                },
                'total': len(cleaned_items),
                'filter': {
                    'round': round,
                    'limit': limit,
                    'include_solves': include_solves
                },
                'items': cleaned_items
            }
            
    except APIError as e:
        raise Exception(f"Failed to get {event_id} results for competition {competition_id}: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error getting {event_id} results for competition {competition_id}: {e}")



# This is the main server instance that MCP clients will connect to