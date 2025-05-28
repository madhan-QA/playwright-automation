# pages/api/base_api_client.py
import json
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin

from playwright.sync_api import APIRequestContext, APIResponse


class BaseAPIClient:
    """Base class for API clients using Playwright's request context."""
    
    def __init__(self, request_context, base_url: str):
        self.request_context = request_context
        self.base_url = base_url
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def _setup_logging(self):
        """Set up logging for API requests."""
        logger = logging.getLogger(f"{self.__class__.__name__}")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            # Create file handler
            file_handler = logging.FileHandler("logs/api_automation.log")
            file_handler.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            
            # Add handler to logger
            logger.addHandler(file_handler)
        
        return logger
    
    def _log_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None):
        """Log API request details with full URL."""
        # full_url = self.base_url.rstrip("/") + "/" + endpoint.lstrip("/")
        # self.logger.info(f"API Request: {method.upper()} {full_url}")
        
        if headers:
            self.logger.info(f"Headers: {json.dumps(headers, indent=2)}")
        if data:
            self.logger.info(f"Request Data: {json.dumps(data, indent=2)}")

    
    def _log_response(self, response: APIResponse):
        """Log API response details."""
        self.logger.info(f"Response Status: {response.status}")
        self.logger.info(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_body = response.json()
            self.logger.info(f"Response Body: {json.dumps(response_body, indent=2)}")
        except Exception:
            # If response is not JSON, log as text
            try:
                response_text = response.text()
                self.logger.info(f"Response Text: {response_text[:500]}...")
            except Exception:
                self.logger.info("Response body could not be logged")
    
    def get(self, endpoint: str, params: Dict = None, headers: Dict = None) -> APIResponse:
        """Make GET request."""
        self._log_request("GET", endpoint, headers=headers)
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))  # join properly

        
        response = self.request_context.get(
            endpoint,
            params=params,
            headers=headers
        )
        
        self._log_response(response)
        return response
    
    def post(self, endpoint: str, data: Dict = None, headers: Dict = None) -> APIResponse:
        self._log_request("POST", endpoint, data=data, headers=headers)
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))  # join properly
        
        response = self.request_context.post(
            url,
            data=json.dumps(data) if data else None,
            headers=headers
        )
        
        self._log_response(response)
        return response
    
    def put(self, endpoint: str, data: Dict = None, headers: Dict = None) -> APIResponse:
        """Make PUT request."""
        self._log_request("PUT", endpoint, data=data, headers=headers)
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))  # join properly

        
        response = self.request_context.put(
            endpoint,
            data=json.dumps(data) if data else None,
            headers=headers
        )
        
        self._log_response(response)
        return response
    
    def delete(self, endpoint: str, headers: Dict = None) -> APIResponse:
        """Make DELETE request."""
        self._log_request("DELETE", endpoint, headers=headers)
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))  # join properly

        
        response = self.request_context.delete(
            endpoint,
            headers=headers
        )
        
        self._log_response(response)
        return response
    
    def patch(self, endpoint: str, data: Dict = None, headers: Dict = None) -> APIResponse:
        """Make PATCH request."""
        self._log_request("PATCH", endpoint, data=data, headers=headers)
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))  # join properly

        
        response = self.request_context.patch(
            endpoint,
            data=json.dumps(data) if data else None,
            headers=headers
        )
        
        self._log_response(response)
        return response
    
    def assert_status_code(self, response: APIResponse, expected_status: int):
        """Assert response status code."""
        actual_status = response.status
        assert actual_status == expected_status, (
            f"Expected status {expected_status}, got {actual_status}. "
            f"Response: {response.text()}"
        )
    
    def assert_json_contains(self, response: APIResponse, expected_data: Dict):
        """Assert response JSON contains expected data."""
        response_json = response.json()
        
        for key, expected_value in expected_data.items():
            assert key in response_json, f"Key '{key}' not found in response"
            actual_value = response_json[key]
            assert actual_value == expected_value, (
                f"Expected {key}='{expected_value}', got '{actual_value}'"
            )
    
    def assert_json_schema(self, response: APIResponse, required_fields: list):
        """Assert response JSON has required fields."""
        response_json = response.json()
        
        for field in required_fields:
            assert field in response_json, (
                f"Required field '{field}' not found in response: {response_json}"
            )
    
    def get_json_response(self, response: APIResponse) -> Dict[str, Any]:
        """Get JSON response with error handling."""
        try:
            return response.json()
        except Exception as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            self.logger.error(f"Response text: {response.text()}")
            raise
    
    def wait_for_condition(self, condition_func, timeout: int = 30, interval: int = 2) -> bool:
        """Wait for a condition to be true with polling."""
        import time
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(interval)
        
        return False