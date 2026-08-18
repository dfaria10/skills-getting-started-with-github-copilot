"""
Shared pytest configuration and fixtures for FastAPI tests.
Provides reusable test utilities and isolated state management.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


# Initial activities state for reference
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis skills development and matches",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 8,
        "participants": ["anna@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater performance and acting workshops",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["lucy@mergington.edu", "david@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and sculpture creation",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["megan@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Wednesdays, 3:30 PM - 4:45 PM",
        "max_participants": 14,
        "participants": ["alex@mergington.edu", "ryan@mergington.edu"]
    },
    "Science Club": {
        "description": "Explore scientific experiments and projects",
        "schedule": "Fridays, 3:30 PM - 4:45 PM",
        "max_participants": 16,
        "participants": ["sarah@mergington.edu"]
    }
}


def reset_activities():
    """Reset the in-memory activities database to initial state."""
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES))


@pytest.fixture
def client():
    """FastAPI TestClient for making API requests."""
    return TestClient(app)


@pytest.fixture
def clean_activities():
    """Fixture with isolated activity state reset for each test.
    
    This fixture ensures test isolation by:
    1. Resetting activities to initial state before test
    2. Allowing test to modify activities without affecting other tests
    3. Cleaning up after test completes
    """
    reset_activities()
    yield activities
    reset_activities()


@pytest.fixture
def activities_with_empty_classes():
    """Fixture providing activities with some classes having no participants."""
    reset_activities()
    activities["Art Studio"]["participants"] = []
    activities["Basketball Team"]["participants"] = []
    yield activities
    reset_activities()


@pytest.fixture
def full_activity():
    """Fixture providing an activity at max capacity."""
    reset_activities()
    # Fill Tennis Club to capacity (max 8)
    activities["Tennis Club"]["participants"] = [
        f"student{i}@mergington.edu" for i in range(8)
    ]
    yield activities
    reset_activities()


# Test data constants for parametrization
VALID_EMAILS = [
    "newstudent@mergington.edu",
    "alice.smith@mergington.edu",
    "bob123@mergington.edu",
]

INVALID_EMAILS = [
    "not-an-email",
    "@mergington.edu",
    "student@",
    "",
]

ACTIVITY_NAMES = list(INITIAL_ACTIVITIES.keys())

INVALID_ACTIVITY_NAMES = [
    "Nonexistent Club",
    "Invalid Activity",
    "",
    "12345",
]
