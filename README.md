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

## Use Cases & Examples / 使用案例和示例

### 🏆 Query World Records and Rankings
**User (English)**: "What's the current 3x3x3 world record?"

**AI Response**: The current 3x3x3 world record is 3.05 seconds, held by Xuanyi Geng (耿暄一) from China, set at the Shenzhen Cubing 10th Anniversary 2024 competition.

### 👤 Get Competitor Profiles  
**User (中文)**: "告诉我世界纪录保持者的信息"

**AI Response**: 耿暄一（WCA ID: 2023GENG02）来自中国，保持多项纪录。他参加了48场比赛，在三阶、二阶和金字塔等项目中获得15枚金牌、8枚银牌和4枚铜牌。

### 🗓️ Find Competitions by Date
**User (Español)**: "¿Qué competencias hay el 18 de enero de 2025?"

**AI Response**: Hay 31 competencias programadas para el 18 de enero de 2025, incluyendo eventos en Australia (Geelong Summer 2025), Brasil (Cubo Carioca 2025), Alemania (Franconia Winter 2025), Corea del Sur (Sejong Winter 2025), y muchos otros países.

### 🎯 Search by Event Type
**User (English)**: "Find competitions with 3x3x3 Blindfolded events"

**AI Response**: Here are upcoming competitions featuring 3x3x3 Blindfolded, including competition dates, locations, and registration details.

### 🏅 Championship Information
**User (中文)**: "上一届世界锦标赛是什么时候？"

**AI Response**: 上一届世界锦标赛是2025年WCA世界锦标赛，于2025年7月3-6日在美国西雅图会展中心举行。上上届是2023年WCA世界锦标赛，于2023年8月12-15日在韩国仁川的松道会展中心举办。

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

## Acknowledgements

- **[World Cube Association (WCA)](https://www.worldcubeassociation.org/)** - For maintaining the official speedcubing database and providing competition data
- **[Unofficial WCA API](https://wca-rest-api.robiningelbrecht.be/#section/Introduction)** - For enabling programmatic access to WCA data through their unofficial API endpoints
- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)** - For the fast and efficient protocol that enables seamless AI assistant integration
- **[FastMCP](https://gofastmcp.com/getting-started/welcome)** - For providing the framework to build MCP servers efficiently