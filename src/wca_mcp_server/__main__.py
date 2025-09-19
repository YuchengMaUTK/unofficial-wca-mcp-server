"""Entry point for running the WCA MCP Server."""

import asyncio
from .main import mcp


def main():
    """Main entry point for the WCA MCP Server."""
    try:
        # Run the FastMCP server
        asyncio.run(mcp.run())
    except KeyboardInterrupt:
        print("\nShutting down WCA MCP Server...")
    except Exception as e:
        print(f"Error running WCA MCP Server: {e}")
        raise


if __name__ == "__main__":
    main()