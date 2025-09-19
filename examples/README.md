# Configuration Examples

This directory contains example configuration files for various MCP clients.

## Claude Desktop

Copy the contents of `claude_desktop_config.json` to your Claude Desktop configuration file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## Other MCP Clients

For other MCP clients, use the command:

```bash
wca-mcp-server
```

Or if installed in development mode:

```bash
python -m wca_mcp_server
```

## Environment Variables

You can customize the server behavior with these environment variables:

- `WCA_CACHE_TTL`: Cache time-to-live in seconds (default: 3600)
- `WCA_LOG_LEVEL`: Logging level - DEBUG, INFO, WARNING, ERROR (default: INFO)
- `WCA_API_TIMEOUT`: API request timeout in seconds (default: 30)