"""SimpleFin API service integration."""

import json
import logging
import requests
from typing import Optional
from pathlib import Path
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import Config
from models import SimpleFinAccountResponse, SimpleFINAccount

logger = logging.getLogger(__name__)


class SimpleFinService:
    """Service for interacting with SimpleFin API."""

    def __init__(self, config: Config):
        """Initialize SimpleFin service."""
        self.config = config
        self.base_url = config.access_url
        self.session = requests.Session()
        self._setup_session_with_retries()

    def _setup_session_with_retries(self):
        """Setup session with automatic retry logic."""
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def fetch_accounts(self, start_date: Optional[str] = None) -> SimpleFinAccountResponse:
        """
        Fetch accounts from SimpleFin API.

        Args:
            start_date: Unix timestamp string for filtering transactions

        Returns:
            SimpleFinAccountResponse containing accounts and any errors
        """
        if start_date is None:
            start_date = self.config.start_date

        try:
            url = f"{self.base_url}/accounts?start-date={start_date}"
            logger.info(f"Fetching accounts from SimpleFin API (this may take a moment)...")
            
            # Use longer timeout for SimpleFin API which can be slow
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()
            account_response = SimpleFinAccountResponse.from_dict(data)

            if account_response.errors:
                logger.warning(f"API returned errors: {account_response.errors}")

            return account_response

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch accounts: {e}")
            return SimpleFinAccountResponse(
                accounts=[], errors=[f"API request failed: {str(e)}"]
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response: {e}")
            return SimpleFinAccountResponse(
                accounts=[], errors=[f"Response parsing failed: {str(e)}"]
            )

    def save_response(self, response: SimpleFinAccountResponse, filepath: str) -> bool:
        """
        Save account response to file.

        Args:
            response: SimpleFinAccountResponse to save
            filepath: Path to save the JSON file

        Returns:
            True if successful, False otherwise
        """
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w") as f:
                json.dump(response.to_dict(), f, indent=2)

            logger.info(f"Saved response to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to save response: {e}")
            return False

    def load_response(self, filepath: str) -> Optional[SimpleFinAccountResponse]:
        """
        Load account response from file.

        Args:
            filepath: Path to load the JSON file from

        Returns:
            SimpleFinAccountResponse if successful, None otherwise
        """
        try:
            path = Path(filepath)
            if not path.exists():
                logger.warning(f"File not found: {filepath}")
                return None

            with open(path, "r") as f:
                data = json.load(f)

            response = SimpleFinAccountResponse.from_dict(data)
            logger.info(f"Loaded response from {filepath}")
            return response

        except Exception as e:
            logger.error(f"Failed to load response: {e}")
            return None

    def filter_tracked_accounts(
        self, response: SimpleFinAccountResponse, tracked_names: list[str]
    ) -> list[SimpleFINAccount]:
        """
        Filter accounts to only those in the tracked list.

        Args:
            response: SimpleFinAccountResponse containing all accounts
            tracked_names: List of account names to track

        Returns:
            List of SimpleFINAccount objects that are in tracked_names
        """
        if not tracked_names:
            return response.accounts

        filtered = [
            account
            for account in response.accounts
            if account.name in tracked_names
        ]
        logger.info(
            f"Filtered {len(response.accounts)} accounts to {len(filtered)} tracked accounts"
        )
        return filtered

    def get_or_fetch_accounts(
        self,
        cache_filepath: Optional[str] = None,
        use_cache: bool = True,
        start_date: Optional[str] = None,
    ) -> SimpleFinAccountResponse:
        """
        Get accounts, using cache if available.

        Args:
            cache_filepath: Path to cache file
            use_cache: Whether to use cached data if available
            start_date: Unix timestamp for filtering transactions

        Returns:
            SimpleFinAccountResponse
        """
        # Try test data if enabled
        if self.config.use_test_data:
            test_data_path = Path(__file__).parent.parent / "api" / "data" / "simpleFinResp.json"
            logger.info("Using test data from SimpleFin API response")
            return self.load_response(str(test_data_path)) or SimpleFinAccountResponse(
                accounts=[], errors=["Failed to load test data"]
            )

        # Try to load from cache if enabled
        if use_cache and cache_filepath:
            cached_response = self.load_response(cache_filepath)
            if cached_response:
                logger.info("Using cached account data")
                return cached_response

        # Fetch from API
        response = self.fetch_accounts(start_date)

        # Save to cache if filepath provided
        if cache_filepath and not response.errors:
            self.save_response(response, cache_filepath)

        return response
