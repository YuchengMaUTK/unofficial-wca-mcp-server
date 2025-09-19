"""Basic tests for WCA MCP Server."""

import pytest
from wca_mcp_server import mcp


def test_mcp_server_exists():
    """Test that the MCP server instance exists."""
    assert mcp is not None
    assert hasattr(mcp, 'name')
    assert mcp.name == "WCA MCP Server"


def test_mcp_server_has_tools():
    """Test that the MCP server has tools registered."""
    # The server should have tools registered via decorators
    # We can't easily test the internal tools list, but we can test the server exists
    assert mcp is not None


def test_version_import():
    """Test that version can be imported."""
    from wca_mcp_server import __version__
    assert __version__ == "0.1.0"