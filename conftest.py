# conftest.py - Updated with API testing support
import subprocess
import sys
import os
import json
import pytest
import logging
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page, Browser, APIRequestContext

# Import page objects
from pages.login.login_page import LoginPage

load_dotenv()

# ------------------- #
# Utility functions
# ------------------- #
def load_json_config(path: str, create_dirs: bool = False) -> dict:
    """
    Generic JSON loader for config files.
    Args:
        path (str): Path to the JSON file.
        create_dirs (bool): Whether to create parent directories if missing (default False).
    Returns:
        dict: Parsed JSON content or empty dict if error.
    """
    try:
        if create_dirs:
            os.makedirs(os.path.dirname(path), exist_ok=True)

        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        else:
            logging.warning(f"Config file not found: {path}")
            return {}
    except Exception as e:
        logging.error(f"Error loading config from {path}: {str(e)}")
        return {}

# ------------------- #
# Test Markers Configuration
# ------------------- #
def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line("markers", "ui: UI/Browser tests")
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "integration: Integration tests (UI + API)")
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")

# ------------------- #
# Session-level fixtures
# ------------------- #
@pytest.fixture(scope="session")
def login_config(request):
    """Build login config from environment variables and return it."""
    config = {
        "login": {
            "url": os.getenv("BASE_URL"),
            "email": os.getenv("EMAIL"),
            "password": os.getenv("PASSWORD")
        },
        "api": {
            "base_url": os.getenv("API_BASE_URL", os.getenv("BASE_URL")),
            "timeout": int(os.getenv("API_TIMEOUT", "30000"))
        }
    }

    # Optional: Write to login_config.json for other tools or debugging
    config_path = 'data/login_config.json'
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

    # Finalizer to reset login_config.json after all tests
    def reset_config():
        empty_config = {
            "login": {"url": "", "email": "", "password": ""},
            "api": {"base_url": "", "timeout": 30000}
        }
        with open(config_path, 'w') as f:
            json.dump(empty_config, f, indent=4)

    request.addfinalizer(reset_config)
    return config

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Add custom browser context arguments."""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }

# ------------------- #
# UI Testing Fixtures
# ------------------- #
@pytest.fixture(scope="session")
def session_browser(playwright):
    """Create a session-scoped browser."""
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

@pytest.fixture(scope="session")
def session_context(session_browser, browser_context_args):
    """Create a session-scoped browser context."""
    context = session_browser.new_context(**browser_context_args)
    yield context
    context.close()

@pytest.fixture(scope="session")
def session_page(session_context):
    """Create a session-scoped page."""
    page = session_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session")
def authenticated_page(session_page, login_config):
    """
    Session-scoped fixture that logs in once and returns the authenticated page.
    This page can be used for both UI tests and to extract cookies/tokens for API tests.
    """
    page = session_page
    login_page = LoginPage(page)
    
    # Navigate to login page
    page.goto(login_config["login"]["url"], timeout=60000, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")
    
    # Log in
    login_page.login(
        email=login_config["login"]["email"],
        password=login_config["login"]["password"]
    )
    
    # Wait for login to complete
    page.wait_for_load_state("networkidle")
    
    # Return the authenticated page
    yield page

# ------------------- #
# API Testing Fixtures
# ------------------- #
@pytest.fixture(scope="session")
def api_request_context(playwright, login_config):
    """Create a session-scoped API request context."""
    request_context = playwright.request.new_context(
        base_url=login_config["api"]["base_url"],
        extra_http_headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope="session")
def authenticated_api_context(playwright, authenticated_page, login_config):
    """
    Create an authenticated API request context using cookies from the authenticated page.
    This allows API tests to use the same session as UI tests.
    """
    # Get cookies from the authenticated page
    cookies = authenticated_page.context.cookies()
    
    # Prepare extra headers with cookies
    extra_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Add cookies to headers if available
    if cookies:
        cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        extra_headers["Cookie"] = cookie_string
    
    # Create API request context with cookies in headers
    request_context = playwright.request.new_context(
        base_url=login_config["api"]["base_url"],
        extra_http_headers=extra_headers
    )
    
    yield request_context
    request_context.dispose()

@pytest.fixture
def api_client(authenticated_api_context):
    """Provide the authenticated API request context for individual tests."""
    return authenticated_api_context

# ------------------- #
# Shared Test Data Fixtures
# ------------------- #
@pytest.fixture(scope="session")
def api_endpoints():
    """Load API endpoints configuration."""
    return load_json_config('data/api_endpoints.json')

@pytest.fixture(scope="session")
def api_test_data():
    """Load API test data."""
    return load_json_config('data/api_test_data.json')

# ------------------- #
# Integration Testing Fixtures
# ------------------- #
@pytest.fixture
def ui_and_api_clients(authenticated_page, authenticated_api_context):
    """Provide both UI page and API client for integration tests."""
    return {
        "page": authenticated_page,
        "api": authenticated_api_context
    }

# ------------------- #
# Existing Filter Data Function
# ------------------- #
def get_filters_data():
    """Load filter configurations for parameterized tests."""
    data = load_json_config('data/pipeline_filters.json')
    return data.get('filters', [])

# ------------------- #
# Cleanup and Setup Hooks
# ------------------- #
@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Setup and cleanup for each test."""
    # Setup
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)
    
    yield
    
    # Cleanup (if needed)
    pass

def pytest_runtest_makereport(item, call):
    """Generate detailed test reports with screenshots for failures."""
    if call.when == "call" and call.excinfo is not None:
        # Test failed, take screenshot if it's a UI test
        if hasattr(item, "funcargs"):
            if "page" in item.funcargs or "authenticated_page" in item.funcargs:
                try:
                    page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")
                    if page:
                        screenshot_name = f"failure_{item.name}_{call.when}.png"
                        page.screenshot(path=f"screenshots/{screenshot_name}")
                except Exception:
                    pass  # Ignore screenshot errors