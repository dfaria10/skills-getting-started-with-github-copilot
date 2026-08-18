"""
Tests for DELETE /activities/{activity_name}/unregister endpoint.
Validates successful unregistration, error handling, and validation.
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering a student from an activity."""

    def test_unregister_success(self, client, clean_activities):
        """Verify successful unregister removes participant from activity."""
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"
        
        assert email in clean_activities[activity]["participants"]
        
        response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_unregister_removes_participant(self, client, clean_activities):
        """Verify that unregister actually removes the participant."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # Verify student is registered
        assert email in clean_activities[activity]["participants"]
        
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == 200
        
        # Verify student is now unregistered
        assert email not in clean_activities[activity]["participants"]

    def test_unregister_decrements_participant_count(self, client, clean_activities):
        """Verify participant count decreases after unregister."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        initial_count = len(clean_activities[activity]["participants"])
        
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        
        assert response.status_code == 200
        assert len(clean_activities[activity]["participants"]) == initial_count - 1

    def test_unregister_activity_not_found(self, client, clean_activities):
        """Verify unregister fails with 404 for nonexistent activity."""
        response = client.delete(
            "/activities/Nonexistent Club/unregister?email=student@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_student_not_registered(self, client, clean_activities):
        """Verify unregister fails with 400 if student not registered."""
        email = "notregistered@mergington.edu"
        activity = "Chess Club"
        
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"].lower()

    def test_unregister_preserves_other_participants(self, client, clean_activities):
        """Verify unregister doesn't remove other participants."""
        activity = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        other_participant = "daniel@mergington.edu"
        
        # Verify both are registered
        assert email_to_remove in clean_activities[activity]["participants"]
        assert other_participant in clean_activities[activity]["participants"]
        
        response = client.delete(
            f"/activities/{activity}/unregister?email={email_to_remove}"
        )
        
        assert response.status_code == 200
        # Other participant should still be registered
        assert other_participant in clean_activities[activity]["participants"]
        # Removed participant should not be registered
        assert email_to_remove not in clean_activities[activity]["participants"]

    def test_unregister_from_multiple_activities(self, client, clean_activities):
        """Verify unregistering from one activity doesn't affect others."""
        email = "newstudent@mergington.edu"
        
        # Sign up for multiple activities
        client.post(f"/activities/Chess Club/signup?email={email}")
        client.post(f"/activities/Programming Class/signup?email={email}")
        
        # Unregister from Chess Club
        response = client.delete(f"/activities/Chess Club/unregister?email={email}")
        assert response.status_code == 200
        
        # Should be removed from Chess Club
        assert email not in clean_activities["Chess Club"]["participants"]
        
        # Should still be in Programming Class
        assert email in clean_activities["Programming Class"]["participants"]

    def test_unregister_missing_email_parameter(self, client, clean_activities):
        """Verify unregister fails if email parameter is missing."""
        response = client.delete("/activities/Chess Club/unregister")
        
        # FastAPI will return 422 for missing required parameter
        assert response.status_code == 422

    def test_unregister_empty_email(self, client, clean_activities):
        """Verify unregister with empty email fails."""
        response = client.delete("/activities/Chess Club/unregister?email=")
        
        # Empty string might be treated as validation error
        assert response.status_code != 200

    def test_unregister_same_student_twice(self, client, clean_activities):
        """Verify unregistering same student twice fails on second attempt."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # First unregister should succeed
        response1 = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response1.status_code == 200
        
        # Second unregister should fail (not registered anymore)
        response2 = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response2.status_code == 400
        data = response2.json()
        assert "not registered" in data["detail"].lower()

    def test_unregister_response_message_format(self, client, clean_activities):
        """Verify unregister response message contains email and activity."""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        data = response.json()
        
        assert email in data["message"]
        assert activity in data["message"]

    def test_unregister_all_participants(self, client, clean_activities):
        """Verify unregistering all participants from activity works."""
        activity = "Tennis Club"
        participants = clean_activities[activity]["participants"].copy()
        
        # Unregister all participants
        for email in participants:
            response = client.delete(f"/activities/{activity}/unregister?email={email}")
            assert response.status_code == 200
        
        # Activity should have no participants
        assert len(clean_activities[activity]["participants"]) == 0
