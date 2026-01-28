"""Data models for SimpleFin integration."""

from dataclasses import dataclass, asdict
from typing import List, Optional
from datetime import datetime


@dataclass
class Transaction:
    """Represents a financial transaction."""

    id: str
    posted: int
    amount: str
    description: str
    account_id: Optional[str] = None

    def to_dict(self):
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class SimpleFINAccount:
    """Represents a SimpleFin account."""

    id: str
    name: str
    currency: str
    balance: str
    balance_date: int
    available_balance: Optional[str] = None
    transactions: Optional[List[Transaction]] = None

    def to_dict(self):
        """Convert to dictionary."""
        data = asdict(self)
        if self.transactions:
            data["transactions"] = [t.to_dict() for t in self.transactions]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "SimpleFINAccount":
        """Create from dictionary."""
        transactions = []
        if "transactions" in data and data["transactions"]:
            transactions = [
                Transaction(
                    id=t["id"],
                    posted=t["posted"],
                    amount=t["amount"],
                    description=t["description"],
                )
                for t in data["transactions"]
            ]

        return cls(
            id=data["id"],
            name=data["name"],
            currency=data["currency"],
            balance=data["balance"],
            balance_date=data["balance-date"],
            available_balance=data.get("available-balance"),
            transactions=transactions,
        )


@dataclass
class SimpleFinAccountResponse:
    """Represents the response from SimpleFin API."""

    accounts: List[SimpleFINAccount]
    errors: List[str]

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "accounts": [a.to_dict() for a in self.accounts],
            "errors": self.errors,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SimpleFinAccountResponse":
        """Create from dictionary."""
        accounts = [
            SimpleFINAccount.from_dict(a) for a in data.get("accounts", [])
        ]
        errors = data.get("errors", [])
        return cls(accounts=accounts, errors=errors)
