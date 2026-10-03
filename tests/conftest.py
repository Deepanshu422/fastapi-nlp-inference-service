import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.model_registry import ModelRegistry


@pytest.fixture(scope="session")
def client():
    """Initializes the FastAPI TestClient and ensures models are loaded for the test session."""
    # Ensure models are loaded once for all tests
    ModelRegistry.load_models()
    with TestClient(app) as test_client:
        yield test_client