"""Configuration management for SimpleFin integration."""

import os
from typing import List
from dotenv import load_dotenv


class Config:
    """Configuration class for SimpleFin integration."""

    def __init__(self):
        """Load environment variables and initialize configuration."""
        load_dotenv()
        self.access_url: str = os.getenv("ACCESS_URL", "")
        self.setup_token: str = os.getenv("SETUP_TOKEN", "")
        self.tracked_accounts: List[str] = os.getenv("TRACKED_ACCOUNTS", "").split(",") if os.getenv("TRACKED_ACCOUNTS") else []
        self.start_date: str = os.getenv("START_DATE", "978360153")  # Unix timestamp
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.use_test_data: bool = os.getenv("USE_TEST_DATA", "false").lower() == "true"

    def validate(self) -> bool:
        """Validate that required configuration is set."""
        if not self.access_url:
            raise ValueError("ACCESS_URL environment variable is not set")
        return True


def load_config() -> Config:
    """Load and return configuration."""
    return Config()
