# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-09-18

### Added
- Initial release of WCA MCP Server
- FastMCP 2.0 based Model Context Protocol server
- Comprehensive WCA data access through static API
- Reference data tools (events, countries, continents)
- Competition search and details tools
- Competitor profile lookup by WCA ID
- World and regional rankings by event
- Competition results with intelligent filtering
- Championship search and details
- Smart result filtering for LLM-friendly responses
- Configurable caching and logging
- Complete type hints and error handling

### Features
- **11 MCP tools** for comprehensive WCA data access
- **Intelligent result filtering** - defaults to Final round only for better LLM processing
- **99.7% size reduction** for competition results (522KB → 1.6KB for Final round)
- **Flexible parameters** for round filtering, result limits, and detail levels
- **Backward compatibility** - can still access all rounds when needed
- **Production ready** with proper error handling and logging
- **Easy installation** via pip/uv with CLI entry point

### Technical Details
- Built with FastMCP 2.0 for modern MCP protocol support
- Uses httpx for async HTTP requests with connection pooling
- Pydantic models for data validation and serialization
- Comprehensive error handling with user-friendly messages
- Configurable via environment variables
- Full type hints for better development experience