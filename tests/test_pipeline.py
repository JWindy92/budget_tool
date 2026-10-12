import json
from unittest.mock import Mock, patch

from finance_pipeline.simplefin import ingest_simplefin


def test_ingest_simplefin_writes_account_balances(tmp_path):
    output_path = tmp_path / "account_balances.json"

    mock_response = Mock()
    mock_response.json.return_value = {
        "accounts": [
            {
                "id": "account123",
                "name": "Checking",
                "balance": "2450.75",
                "currency": "USD",
                "transactions": [],
            }
        ]
    }

    with patch(
        "finance_pipeline.simplefin.requests.get",
        return_value=mock_response,
    ) as mock_get:
        ingest_simplefin(
            "https://example.com/simplefin",
            str(output_path),
        )

    mock_get.assert_called_once()
    mock_response.raise_for_status.assert_called_once()

    data = json.loads(output_path.read_text())

    assert data == [
        {
            "id": "account123",
            "name": "Checking",
            "balance": "2450.75",
            "currency": "USD",
        }
    ]
