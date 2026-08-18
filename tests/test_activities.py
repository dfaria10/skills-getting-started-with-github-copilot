"""
Tests for GET /activities endpoint.
Validates structure, counts, and field correctness of activity data.
"""

import pytest


class TestGetActivities:
    """Test suite for fetching all activities."""

    def test_get_activities_returns_all_activities(self, client, clean_activities):
        """Verify that GET /activities returns all activities."""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check all activities are present
        assert len(data) == len(clean_activities)
        for activity_name in clean_activities.keys():
            assert activity_name in data

    def test_get_activities_returns_correct_structure(self, client, clean_activities):
        """Verify that each activity has required fields."""
        response = client.get("/activities")
        data = response.json()
        
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(set(activity_data.keys()))

    def test_activity_participants_is_list(self, client, clean_activities):
        """Verify that participants field is a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list)
            # Each participant should be a string (email)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)

    def test_get_activities_preserves_participant_count(self, client, clean_activities):
        """Verify that participant counts are accurate."""
        response = client.get("/activities")
        data = response.json()
        
        # Chess Club should have 2 participants
        assert len(data["Chess Club"]["participants"]) == 2
        # Programming Class should have 2 participants
        assert len(data["Programming Class"]["participants"]) == 2
        # Gym Class should have 2 participants
        assert len(data["Gym Class"]["participants"]) == 2

    def test_get_activities_with_empty_classes(self, client, activities_with_empty_classes):
        """Verify activities with no participants are returned correctly."""
        response = client.get("/activities")
        data = response.json()
        
        # Art Studio and Basketball Team should have empty participant lists
        assert data["Art Studio"]["participants"] == []
        assert data["Basketball Team"]["participants"] == []

    def test_get_activities_has_max_participants(self, client, clean_activities):
        """Verify max_participants field is present and correct."""
        response = client.get("/activities")
        data = response.json()
        
        # Chess Club max is 12
        assert data["Chess Club"]["max_participants"] == 12
        # Tennis Club max is 8
        assert data["Tennis Club"]["max_participants"] == 8
        # Gym Class max is 30
        assert data["Gym Class"]["max_participants"] == 30

    def test_get_activities_has_schedule(self, client, clean_activities):
        """Verify schedule field is present."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "schedule" in activity_data
            assert isinstance(activity_data["schedule"], str)
            assert len(activity_data["schedule"]) > 0

    def test_get_activities_has_description(self, client, clean_activities):
        """Verify description field is present."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert isinstance(activity_data["description"], str)
            assert len(activity_data["description"]) > 0
