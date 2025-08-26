"""
Tests for the FastAPI server
"""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from orchael_sdk.server import app


class MockProcessor:
    """Mock processor for testing"""

    def process_chat(self, chat_input: dict) -> dict:  # type: ignore[type-arg]
        return {
            "input": chat_input["input"],
            "output": f"Mock response to: {chat_input['input']}",
        }

    def get_history(self) -> list[dict] | None:  # type: ignore[type-arg]
        return [
            {"input": "test input 1", "output": "test output 1"},
            {"input": "test input 2", "output": "test output 2"},
        ]


@pytest.fixture
def client() -> TestClient:
    """Test client for FastAPI app"""
    return TestClient(app)


@pytest.fixture
def mock_processor() -> MockProcessor:
    """Mock processor instance"""
    return MockProcessor()


def test_health_endpoint(client: TestClient) -> None:
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("orchael_sdk.server.get_processor")
def test_chat_endpoint(
    mock_get_processor: MagicMock,
    client: TestClient,
    mock_processor: MockProcessor,
) -> None:
    """Test the chat endpoint"""
    mock_get_processor.return_value = mock_processor

    chat_request = {"input": "Hello, world!", "history": []}
    response = client.post("/chat", json=chat_request)

    assert response.status_code == 200
    data = response.json()
    assert data["input"] == "Hello, world!"
    assert data["output"] == "Mock response to: Hello, world!"


@patch("orchael_sdk.server.get_processor")
def test_chat_history_endpoint(
    mock_get_processor: MagicMock,
    client: TestClient,
    mock_processor: MockProcessor,
) -> None:
    """Test the chat history endpoint"""
    mock_get_processor.return_value = mock_processor

    response = client.get("/chat/history")

    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert len(data["history"]) == 2
    assert data["history"][0]["input"] == "test input 1"
    assert data["history"][0]["output"] == "test output 1"


def test_chat_endpoint_with_history(
    client: TestClient,
    mock_processor: MockProcessor,
) -> None:
    """Test the chat endpoint with history"""
    with patch("orchael_sdk.server.get_processor") as mock_get_processor:
        mock_processor = MockProcessor()
        mock_get_processor.return_value = mock_processor

        chat_request = {
            "input": "Hello, world!",
            "history": [{"input": "Previous message", "output": "Previous response"}],
        }
        response = client.post("/chat", json=chat_request)

        assert response.status_code == 200
        data = response.json()
        assert data["input"] == "Hello, world!"
        assert data["output"] == "Mock response to: Hello, world!"
