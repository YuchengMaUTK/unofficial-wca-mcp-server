# Unofficial WCA MCP Server

An unofficial Model Context Protocol (MCP) server that provides AI assistants with access to World Cube Association (WCA) speedcubing data.

## Overview

This unofficial WCA MCP Server enables AI assistants to answer questions about speedcubing, including:

- 🏆 Current world records and rankings
- 👤 Competitor profiles and achievements  
- 🏁 Competition information and results
- 🏅 Championship results and details

> **Note**: This is an unofficial project and is not affiliated with the World Cube Association.

## Installation

```bash
git clone https://github.com/YuchengMaUTK/unofficial-wca-mcp-server.git
cd unofficial-wca-mcp-server
pip install -e .
```

## Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "wca": {
      "command": "python",
      "args": ["-m", "wca_mcp_server"]
    }
  }
}
```

## Available Tools

- `get_wca_events`: Get all official WCA events
- `get_wca_countries`: Get all WCA countries  
- `get_wca_continents`: Get all continents
- `get_person_by_wca_id`: Get competitor profile by WCA ID
- `get_rankings`: Get world/regional rankings by event
- `search_competitions_by_date`: Find competitions on a specific date
- `search_competitions_by_event`: Find competitions with a specific event
- `get_competition_by_id`: Get competition details
- `get_competition_results`: Get all results for a competition
- `get_competition_event_results`: Get event-specific results with filtering
- `search_championships`: Search championship competitions
- `get_championship_details`: Get championship details

## License

MIT License - see [LICENSE](LICENSE) file for details.