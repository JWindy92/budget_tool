import json
from pathlib import Path

import requests


def ingest_simplefin(
    access_url: str,
    output_path: str = "output/account_balances.json",
) -> None:
    response = requests.get(
        f"{access_url.rstrip('/')}/accounts",
        timeout=30,
    )
    response.raise_for_status()

    accounts = response.json().get("accounts", [])

    balances = [
        {
            "id": account.get("id"),
            "name": account.get("name"),
            "balance": account.get("balance"),
            "currency": account.get("currency"),
        }
        for account in accounts
    ]

    Path(output_path).write_text(
        json.dumps(balances, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    ingest_simplefin(ACCESS_URL)
