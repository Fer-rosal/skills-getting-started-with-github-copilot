import copy
import os
import sys

import pytest

# Make `src/` importable when running tests from the repo root.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app, activities as _activities  # noqa: E402


@pytest.fixture
def fastapi_client():
    """Provides a TestClient instance for the FastAPI app."""
    from fastapi.testclient import TestClient

    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict before/after each test."""
    original = copy.deepcopy(_activities)
    yield
    _activities.clear()
    _activities.update(copy.deepcopy(original))
