import copy

from fastapi.testclient import TestClient
import pytest

from src.app import app, activities as activities_store


@pytest.fixture
def app_client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(activities_store)
    yield
    activities_store.clear()
    activities_store.update(copy.deepcopy(original))
