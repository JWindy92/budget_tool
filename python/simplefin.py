"""SimpleFin API client."""

import os
import requests
from dotenv import load_dotenv


class SimpleFin:
    """Simple SimpleFin API client."""

    def __init__(self):
        """Initialize with access URL from environment."""
        load_dotenv()
        self.access_url = os.getenv("ACCESS_URL")
        if not self.access_url:
            raise ValueError("ACCESS_URL not set in environment")

    def GetAccounts(self):
        """Fetch and return accounts from SimpleFin API."""
        response = requests.get(f"{self.access_url}/accounts", timeout=30)
        response.raise_for_status()
        return response.json().get("accounts", [])

    def GetAccount(self, account_id, start_date="20260104"):
        start_epoch = YYYYMMDD_to_epoch(start_date)
        """Fetch and return a specific account by ID."""
        response = requests.get(f"{self.access_url}/accounts?account={account_id}&start-date={start_epoch}", timeout=30)
        response.raise_for_status()
        return response.json()

def YYYYMMDD_to_epoch(date_str: str) -> int:
    """Convert YYYYMMDD date string to Unix epoch timestamp."""
    from datetime import datetime
    dt = datetime.strptime(date_str, "%Y%m%d")
    return int(dt.timestamp())

def epoch_to_YYYYMMDD(epoch: int) -> str:
    """Convert Unix epoch timestamp to YYYYMMDD date string."""
    from datetime import datetime
    dt = datetime.fromtimestamp(epoch)
    return dt.strftime("%Y%m%d")