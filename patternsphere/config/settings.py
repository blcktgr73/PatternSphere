"""
Configuration settings for PatternSphere.

Uses Pydantic Settings for environment variable support and type validation.
Settings can be overridden via PATTERNSPHERE_* environment variables.
"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings with environment variable support.

    Environment variables:
    - PATTERNSPHERE_DATA_DIR: Override default data directory
    - PATTERNSPHERE_DEFAULT_LIMIT: Default result limit for searches
    - PATTERNSPHERE_TERMINAL_WIDTH: Terminal width for formatting

    Example:
        export PATTERNSPHERE_DATA_DIR=/custom/data/path
        export PATTERNSPHERE_DEFAULT_LIMIT=50
    """

    model_config = SettingsConfigDict(
        env_prefix="PATTERNSPHERE_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Data paths
    data_dir: Path = Path("data")
    sources_dir: Path = Path("data/sources")
    oorp_patterns_file: Path = Path("data/sources/oorp/oorp_patterns_complete.json")

    # CLI defaults
    default_limit: int = 20
    terminal_width: int = 80

    # Application metadata
    app_name: str = "PatternSphere"
    app_version: str = "1.0.0"
    app_description: str = "A unified knowledge base for software design patterns"

    # Logging
    log_level: str = "INFO"

    def get_absolute_path(self, path: Path) -> Path:
        """Convert relative path to absolute, resolving from project root."""
        if path.is_absolute():
            return path
        # Try to find project root
        current = Path.cwd()
        # Check if we're in the project root or a subdirectory
        if (current / "data").exists():
            return current / path
        # Try parent directories
        for parent in [current] + list(current.parents):
            if (parent / "data").exists():
                return parent / path
        # Fall back to current directory
        return current / path


# Global settings instance
settings = Settings()
