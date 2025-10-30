"""
Tests for the main FastAPI application endpoints
"""
import pytest
from fastapi import status


class TestMainEndpoints:
    """Test main application endpoints"""
    
    def test_root_endpoint_redirects_to_static(self, client):
        """Test that root endpoint redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers["location"] == "/static/index.html"
    
    def test_get_activities(self, client):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        
        # Check structure of first activity
        activity_name = list(data.keys())[0]
        activity = data[activity_name]
        
        required_fields = ["description", "schedule", "max_participants", "participants"]
        for field in required_fields:
            assert field in activity
        
        assert isinstance(activity["participants"], list)
        assert isinstance(activity["max_participants"], int)


class TestSignupEndpoint:
    """Test activity signup functionality"""
    
    def test_successful_signup(self, client, reset_activities, sample_email):
        """Test successful signup for an activity"""
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email={sample_email}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert activity_name in data["message"]
    
    def test_signup_nonexistent_activity(self, client, sample_email):
        """Test signup for non-existent activity"""
        activity_name = "Nonexistent Activity"
        
        response = client.post(f"/activities/{activity_name}/signup?email={sample_email}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_duplicate_signup(self, client, reset_activities, sample_email):
        """Test that duplicate signup is prevented"""
        activity_name = "Chess Club"
        
        # First signup should succeed
        response1 = client.post(f"/activities/{activity_name}/signup?email={sample_email}")
        assert response1.status_code == status.HTTP_200_OK
        
        # Second signup should fail
        response2 = client.post(f"/activities/{activity_name}/signup?email={sample_email}")
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response2.json()
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_with_existing_participant(self, client, reset_activities):
        """Test signup with email that's already in participants list"""
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        
        response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "already signed up" in data["detail"].lower()


class TestUnregisterEndpoint:
    """Test activity unregister functionality"""
    
    def test_successful_unregister(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already registered
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={existing_email}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert existing_email in data["message"]
        assert activity_name in data["message"]
        assert "unregistered" in data["message"].lower()
    
    def test_unregister_nonexistent_activity(self, client, sample_email):
        """Test unregister from non-existent activity"""
        activity_name = "Nonexistent Activity"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={sample_email}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert data["detail"] == "Activity not found"
    
    def test_unregister_not_registered_participant(self, client, reset_activities, sample_email):
        """Test unregister participant who is not registered"""
        activity_name = "Chess Club"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={sample_email}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "not registered" in data["detail"].lower()
    
    def test_signup_then_unregister_workflow(self, client, reset_activities, sample_email):
        """Test complete workflow: signup then unregister"""
        activity_name = "Programming Class"
        
        # First, sign up
        signup_response = client.post(f"/activities/{activity_name}/signup?email={sample_email}")
        assert signup_response.status_code == status.HTTP_200_OK
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert sample_email in activities_data[activity_name]["participants"]
        
        # Then unregister
        unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={sample_email}")
        assert unregister_response.status_code == status.HTTP_200_OK
        
        # Verify participant was removed
        activities_response2 = client.get("/activities")
        activities_data2 = activities_response2.json()
        assert sample_email not in activities_data2[activity_name]["participants"]


class TestDataIntegrity:
    """Test data integrity and edge cases"""
    
    def test_activities_data_structure(self, client):
        """Test that activities data has correct structure"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_details in data.items():
            assert isinstance(activity_name, str)
            assert len(activity_name) > 0
            
            assert "description" in activity_details
            assert "schedule" in activity_details
            assert "max_participants" in activity_details
            assert "participants" in activity_details
            
            assert isinstance(activity_details["description"], str)
            assert isinstance(activity_details["schedule"], str)
            assert isinstance(activity_details["max_participants"], int)
            assert isinstance(activity_details["participants"], list)
            
            assert activity_details["max_participants"] > 0
            assert len(activity_details["participants"]) <= activity_details["max_participants"]
    
    def test_email_format_in_participants(self, client):
        """Test that participant emails contain @ symbol"""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_details in data.items():
            for participant in activity_details["participants"]:
                assert "@" in participant
                assert participant.endswith("@mergington.edu")
    
    def test_multiple_activities_signup(self, client, reset_activities, sample_email):
        """Test signing up for multiple different activities"""
        activities_to_test = ["Chess Club", "Programming Class", "Art Club"]
        
        for activity_name in activities_to_test:
            response = client.post(f"/activities/{activity_name}/signup?email={sample_email}")
            assert response.status_code == status.HTTP_200_OK
        
        # Verify user is registered for all activities
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        for activity_name in activities_to_test:
            assert sample_email in activities_data[activity_name]["participants"]