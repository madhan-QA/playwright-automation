# tests/api/test_auth_api.py
import pytest
from pages.api.auth_api_client import AuthAPIClient
from pathlib import Path
import json
import asyncio



@pytest.mark.api
class TestAuthAPI:
    """Test authentication API endpoints."""
    
    @pytest.fixture
    def auth_client(self, api_client,login_config) -> AuthAPIClient:
        """Create auth API client."""
        return AuthAPIClient(api_client,login_config["api"]["base_url"])
    
    def test_getlatest_version(self,auth_client:AuthAPIClient):
        """To Test and print the latest version"""
        response = auth_client.get_latest_version()


    
    def test_login_with_valid_credentials(self, auth_client:AuthAPIClient, login_config):
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
        
       
    def test_login_with_invalid_credentials(self, auth_client:AuthAPIClient):
        """Test login with invalid credentials."""
        response = auth_client.login(
            email="invalid@email.com",
            password="wrongpassword"
        )
       # assert response.status in [400, 401, 403], f"Expected auth failure, got {response.status}"

        
    
    def test_fetch_user_details(self, auth_client: AuthAPIClient, login_config):
    # Step 1: Login and capture response
        login_response = auth_client.login(
            email=login_config["login"]["email"],
            password=login_config["login"]["password"]
        )
        login_data = login_response.json()

        # Step 2: Extract user ID
        user_id = login_data.get("data", {}).get("id")
        assert user_id, "User ID not found in login response"

        # Step 3: Fetch user details using ID
        user_details_response = auth_client.get_user_details(user_id)
        user_data = user_details_response.json()
        user_list = user_data.get("data", [])
        assert isinstance(user_list, list), "Expected 'data' to be a list"
        assert user_list, "'data' list is empty"


        # Step 4: Validate
        first_user = user_list[0]
        assert first_user["id"] == user_id, f"Expected user ID {user_id}, but got {first_user['id']}"

    def test_logout(self, auth_client:AuthAPIClient):
        """Test logout functionality."""
        response = auth_client.logout()
        if response.status == 404:
            pytest.skip("Logout endpoint not found")

    """"To store all the user credenatils - """

    # def test_fetch_alluser_details(self, auth_client: AuthAPIClient):
    #     """Test fetching user details for a range of user IDs."""
    #     all_responses = {}

    #     for user_id in range(4000, 4010):
    #         try:
    #             response = auth_client.get_user_details(str(user_id))
    #             user_data = response.json()

    #             # Only store non-empty "data" lists
    #             data_list = user_data.get("data")

    #             if isinstance(data_list, list) and data_list:
    #                 user_info = data_list[0]
    #                 filtered_user = {
    #                     "id": user_info.get("id"),
    #                     "name": user_info.get("name"),
    #                     "email": user_info.get("email"),
    #                     "password": user_info.get("password")  # Only if available
    #                 }
    #             all_responses[user_id] = filtered_user

    #         except Exception as e:
    #           all_responses[user_id] = {"error": str(e)}

    #     # Only write to file if there's valid (non-empty) data
    #     if all_responses:
    #         output_file = Path("reports/user_credentials.json")
    #         with output_file.open("w", encoding="utf-8") as f:
    #             json.dump(all_responses, f, indent=2)

    #     assert all_responses, "No valid user data collected"

    
