"""Configuration management for the WCA MCP Server."""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_prefix="WCA_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # API Configuration
    api_base_url: str = Field(
        default="https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api",
        description="Base URL for the WCA API"
    )
    api_timeout: int = Field(
        default=30,
        description="API request timeout in seconds"
    )
    
    # Caching Configuration
    cache_ttl: int = Field(
        default=3600,
        description="Cache time-to-live in seconds"
    )
    cache_max_size: int = Field(
        default=1000,
        description="Maximum number of items in cache"
    )
    
    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    
    # Server Configuration
    server_name: str = Field(
        default="WCA MCP Server",
        description="Name of the MCP server"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()