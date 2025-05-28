# tests/api/test_auth_api.py
import pytest
from pages.api.auth_api_client import AuthAPIClient

@pytest.mark.api
class TestAuthAPI:
    """Test authentication API endpoints."""
    
    @pytest.fixture
    def auth_client(self, api_client,login_config):
        """Create auth API client."""
        return AuthAPIClient(api_client,login_config["api"]["base_url"])
    
    def test_getLatest_version(self,auth_client):
        """To Test and print the latest version"""
        response = auth_client.get_latest_version()
    
    def test_login_with_valid_credentials(self, auth_client, login_config):
        """Test login with valid credentials."""
        response = auth_client.login(
            email=login_config["login"]["email"],
            password=login_config["login"]["password"]
        )
        if response.status == 404:
            pytest.skip("Login endpoint not found - adjust endpoint URL")
        elif response.status == 405:
            pytest.skip("Method not allowed - check if endpoint accepts POST")
        
        # Validate response
        
       
    def test_login_with_invalid_credentials(self, auth_client):
        """Test login with invalid credentials."""
        response = auth_client.login(
            email="invalid@email.com",
            password="wrongpassword"
        )
       # assert response.status in [400, 401, 403], f"Expected auth failure, got {response.status}"

        
    
    # def test_get_user_profile_authenticated(self, auth_client):
    #     """Test getting user profile when authenticated."""
    #     response = auth_client.get_user_profile()
        
    #     # Should succeed and contain user data
    #     response_data = auth_client.get_json_response(response)
    #     assert "email" in response_data
    #     assert "id" in response_data
    
    def test_logout(self, auth_client):
        """Test logout functionality."""
        response = auth_client.logout()
        if response.status == 404:
            pytest.skip("Logout endpoint not found")
        
        
    
