"""
Test configuration and fixtures for FastAPI tests
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to original state after each test"""
    # Store original state
    original_activities = {
        name: {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": details["participants"].copy()
        }
        for name, details in activities.items()
    }
    
    yield
    
    # Reset to original state
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def sample_activity_name():
    """Return a sample activity name for testing"""
    return "Chess Club"


@pytest.fixture
def sample_email():
    """Return a sample email for testing"""
    return "test@mergington.edu"