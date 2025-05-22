# conftest.py - Place this file in your project root or test directory
import subprocess
import sys
import os
import json
import pytest
import logging
from playwright.sync_api import sync_playwright, Page, Browser

# Import page objects
from pages.login.login_page import LoginPage

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


@pytest.fixture(scope="session")
def login_config():
    """Session-scoped fixture that provides login configuration."""
    return load_json_config('data/login_config.json', create_dirs=True)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Add custom browser context arguments."""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720,
        },
        "ignore_https_errors": True,
    }


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



# Common filter data accessor function
def get_filters_data():
    """Load filter configurations for parameterized tests."""
    data = load_json_config('data/pipeline_filters.json')
    return data.get('filters', [])