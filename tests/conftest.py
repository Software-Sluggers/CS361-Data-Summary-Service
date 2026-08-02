import os

import pytest
import requests

PORT = os.environ.get("PORT", "5000")
BASE_URL = f"http://localhost:{PORT}"


def pytest_sessionstart(session: pytest.Session):
    """Fail the suite immediately if the Docker service is not healthy."""

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        response.raise_for_status()
        if response.json().get("status") != "ok":
            raise ValueError()
    except (requests.RequestException, ValueError):
        pytest.exit(
            "Container is not healthy. Did you run `docker compose up`?", returncode=1
        )


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def post_summary(base_url: str):
    """POST JSON to /summary and return (status_code, response_body)."""

    def _post(payload: object) -> tuple[int, dict]:
        response = requests.post(f"{base_url}/summary", json=payload, timeout=5)
        return response.status_code, response.json()

    return _post
