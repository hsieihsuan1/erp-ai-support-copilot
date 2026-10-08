"""Explicit mocks inspired by the source's ServiceNow/Jira interface.
No URLs, HTTP requests, provider configuration or implicit live fallback.
"""
from typing import Literal


def create_mock_ticket(provider: Literal["servicenow", "jira"], session_id: str, transcript: list[dict], number: int) -> dict:
    prefix = "MOCK-INC" if provider == "servicenow" else "MOCK-JIRA"
    return {"id": f"{prefix}-{number:04d}", "provider": provider, "mode": "mock",
            "session_id": session_id, "transcript": [dict(turn) for turn in transcript],
            "notice": "Simulated locally. Nothing sent to ServiceNow or Jira."}
