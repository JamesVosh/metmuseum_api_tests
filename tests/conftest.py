import pytest
from httpx import Client
from log import log_request, log_response

@pytest.fixture
def client_info():
    with Client(
        base_url="https://collectionapi.metmuseum.org/public/collection/",
        headers={
            "User-Agent": (
                    "AppleWebKit/537.36 (KHTML, like Gecko)"
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    "Chrome/150.0.0.0 YaBrowser/26.8.0.0 Safari/537.36"
            )
        },
        timeout=30,
        event_hooks={"request": [log_request],
                     "response": [log_response]}
    ) as client_0:
        yield client_0
