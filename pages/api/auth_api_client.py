# pages/api/auth_api_client.py
from typing import Dict, Any
import base64
from playwright.sync_api import APIResponse
from pages.api.base_api_client import BaseAPIClient


class AuthAPIClient(BaseAPIClient):
    """API client for authentication-related endpoints."""
    def __init__(self, request_context, base_url: str):
        super().__init__(request_context, base_url)
    
    def login(self, email: str, password: str) -> APIResponse:
        """Login via API."""

        encode_password= base64.b64encode(password.encode("utf-8")).decode("utf-8")
        self.logger.info(f"encoded password :{encode_password}")
        login_data = {
            "email": email,
            "password": encode_password
        }
        
        response = self.post("/login", data=login_data)
        self.assert_status_code(response, 200)
        
        return response
    
    def get_latest_version(self)-> APIResponse:
        """get latest version of the API"""
        response =self.post("/user/fetchLatestVersion")
        self.assert_status_code(response, 200)

        response_json = response.json()
        version = response_json["data"][0]["version"]

        self.logger.info(f"Version fetched from response: {version}")

        self.assert_json_schema(response, ["status", "data", "msg"])
        self.assert_json_contains(response, {
        "status": 1,
        "msg": "Data Fetched Successfully"
    })


    
    def logout(self) -> APIResponse:
        """Logout via API."""
        response = self.post("/logout")
        self.assert_status_code(response, 200)
        self.assert_json_schema(response, ["status", "msg"])
        self.assert_json_contains(response, {
        "status": 1,
        "msg": "User Loggedout Successfully"
    })
       
        return response
    
    def get_user_profile(self) -> APIResponse:
        """Get current user profile."""
        response = self.get("/api/user/profile")
        self.assert_status_code(response, 200)
        
        return response
    
    def verify_token(self, token: str) -> APIResponse:
        """Verify authentication token."""
        headers = {"Authorization": f"Bearer {token}"}
        response = self.get("/api/auth/verify", headers=headers)
        
        return response
    
    def refresh_token(self, refresh_token: str) -> APIResponse:
        """Refresh authentication token."""
        data = {"refresh_token": refresh_token}
        response = self.post("/api/auth/refresh", data=data)
        
        return response
    
    def change_password(self, current_password: str, new_password: str) -> APIResponse:
        """Change user password."""
        data = {
            "current_password": current_password,
            "new_password": new_password
        }
        
        response = self.post("/api/user/change-password", data=data)
        self.assert_status_code(response, 200)
        
        return response
    
    def get_login_token_from_response(self, login_response: APIResponse) -> str:
        """Extract login token from response."""
        response_data = self.get_json_response(login_response)
        
        # Adjust this based on your API response structure
        if "token" in response_data:
            return response_data["token"]
        elif "access_token" in response_data:
            return response_data["access_token"]
        else:
            raise ValueError(f"No token found in login response: {response_data}")
    
    def get_user_id_from_response(self, response: APIResponse) -> str:
        """Extract user ID from response."""
        response_data = self.get_json_response(response)
        
        if "user_id" in response_data:
            return response_data["user_id"]
        elif "id" in response_data:
            return response_data["id"]
        else:
            raise ValueError(f"No user ID found in response: {response_data}")
    
def validate_login_response(self, response: APIResponse):
    """Validate login response has required fields and values."""
    response_data = self.get_json_response(response)
    
    # Basic structure check
    assert "status" in response_data, "Missing 'status' in response"
    assert response_data["status"] == 1, "Login failed, 'status' is not 1"
    
    assert "data" in response_data, "Missing 'data' section in response"
    user_data = response_data["data"]

    # Required user fields
    required_user_fields = [
        "id", "email", "name", "user_type", "region_id",
        "country_id", "distributor_id", "language_code"
    ]
    for field in required_user_fields:
        assert field in user_data, f"Missing required field: {field}"
        assert user_data[field] is not None and user_data[field] != "", f"{field} should not be empty"

    # Optional: Validate structure of available_language
    assert "available_language" in response_data, "Missing 'available_language'"
    assert isinstance(response_data["available_language"], list), "'available_language' should be a list"
    assert len(response_data["available_language"]) > 0, "'available_language' should not be empty"

    # Additional assertions
    assert "email" in user_data, "Email is missing in user data"
