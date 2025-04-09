"""
Configuration module for the PyQt6 desktop application.
Uses pydantic-settings to manage application settings.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """
    Application configuration class.
    Uses pydantic-settings to manage environment variables and configuration.
    """

    # OpenAI API settings
    OPEN_AI_API_KEY: Optional[str] = None
    AI_MODEL_NAME: str = "gpt-4o"

    # Application paths
    APP_DIR: Path = Path(__file__).parent.parent.parent

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


# Create a global instance of the config
config = AppConfig()
