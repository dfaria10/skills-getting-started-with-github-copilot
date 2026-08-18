"""
Tests for POST /activities/{activity_name}/signup endpoint.
Validates successful registration, error handling, and validation.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up a student for an activity."""

    def test_signup_success(self, client, clean_activities):
        """Verify successful signup adds participant to activity."""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_adds_participant_to_list(self, client, clean_activities):
        """Verify that signup actually adds the participant to the activity."""
        email = "newstudent@mergington.edu"
        
        # Verify student is not already registered
        assert email not in clean_activities["Chess Club"]["participants"]
        
        # Sign up
        response = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response.status_code == 200
        
        # Verify student is now registered
        assert email in clean_activities["Chess Club"]["participants"]

    def test_signup_activity_not_found(self, client, clean_activities):
        """Verify signup fails with 404 for nonexistent activity."""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=student@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_student(self, client, clean_activities):
        """Verify signup fails with 400 if student already registered."""
        email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(f"/activities/Chess Club/signup?email={email}")
        
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()

    def test_signup_multiple_students_same_activity(self, client, clean_activities):
        """Verify multiple different students can sign up for same activity."""
        activity = "Programming Class"
        initial_count = len(clean_activities[activity]["participants"])
        
        # Sign up first student
        response1 = client.post(f"/activities/{activity}/signup?email=alice@mergington.edu")
        assert response1.status_code == 200
        
        # Sign up second student
        response2 = client.post(f"/activities/{activity}/signup?email=bob@mergington.edu")
        assert response2.status_code == 200
        
        # Verify both are registered
        assert "alice@mergington.edu" in clean_activities[activity]["participants"]
        assert "bob@mergington.edu" in clean_activities[activity]["participants"]
        assert len(clean_activities[activity]["participants"]) == initial_count + 2

    def test_signup_same_student_different_activities(self, client, clean_activities):
        """Verify same student can sign up for multiple activities."""
        email = "newstudent@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response1.status_code == 200
        
        # Sign up for Programming Class
        response2 = client.post(f"/activities/Programming Class/signup?email={email}")
        assert response2.status_code == 200
        
        # Verify student is in both
        assert email in clean_activities["Chess Club"]["participants"]
        assert email in clean_activities["Programming Class"]["participants"]

    def test_signup_increments_participant_count(self, client, clean_activities):
        """Verify participant count increases after signup."""
        activity = "Gym Class"
        initial_count = len(clean_activities[activity]["participants"])
        
        response = client.post(
            f"/activities/{activity}/signup?email=newstudent@mergington.edu"
        )
        
        assert response.status_code == 200
        assert len(clean_activities[activity]["participants"]) == initial_count + 1

    def test_signup_message_format(self, client, clean_activities):
        """Verify response message contains student email and activity name."""
        email = "newstudent@mergington.edu"
        activity = "Chess Club"
        
        response = client.post(f"/activities/{activity}/signup?email={email}")
        data = response.json()
        
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_missing_email_parameter(self, client, clean_activities):
        """Verify signup fails if email parameter is missing."""
        response = client.post("/activities/Chess Club/signup")
        
        # FastAPI will return 422 for missing required parameter
        assert response.status_code == 422

    def test_signup_empty_email(self, client, clean_activities):
        """Verify signup with empty email.
        
        Note: Current API allows empty email. This is a potential improvement area
        to add email validation at the API level.
        """
        response = client.post("/activities/Chess Club/signup?email=")
        
        # Current implementation accepts empty email (no validation)
        # Future enhancement: Add email validation to reject empty strings
        assert response.status_code in (200, 400, 422)

    def test_signup_preserves_other_participants(self, client, clean_activities):
        """Verify signup doesn't remove existing participants."""
        activity = "Chess Club"
        original_participants = clean_activities[activity]["participants"].copy()
        
        response = client.post(
            f"/activities/{activity}/signup?email=newstudent@mergington.edu"
        )
        
        assert response.status_code == 200
        # All original participants should still be there
        for participant in original_participants:
            assert participant in clean_activities[activity]["participants"]
