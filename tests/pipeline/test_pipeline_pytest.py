
import os
import json
import pytest
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from playwright.sync_api import Page, expect
from bs4 import BeautifulSoup

# Import page objects - adjust import paths based on your structure
from page.login.login_page import LoginPage
from page.pipeline.pipeline_suffciency_page import GraphPage


# ------------------- #
# Pytest fixture to load login configuration
# This can also be moved to `conftest.py` for reuse across other test files
# ------------------- #
@pytest.fixture
def login_config():
    """Load configuration from JSON file with default fallback"""
    try:
        config_path = 'input/login_config.json'
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        else:
            logging.warning(f"Config file not found: {config_path}")
            return {}
    except Exception as e:
        logging.error(f"Error loading config: {str(e)}")
        return {}
    

# ------------------- #
# Test class for Pipeline Dashboard validations
# ------------------- #
class TestPipelineDashboard:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, login_config):
        """
        Autouse fixture to:
        1. Log into the application using the provided config
        2. Navigate to Pipeline Sufficiency dashboard
        3. Store the page and GraphPage object for reuse in tests
        """
        login_page = LoginPage(page)
        
        # Navigate to login page
        page.goto(login_config["login"]["url"], timeout=60000, wait_until="domcontentloaded")
        page.wait_for_load_state("networkidle")
        
        # Perform login
        login_page.login(
            email=login_config["login"]["email"],
            password=login_config["login"]["password"]
        )

        # Navigate to Pipeline Sufficiency page and store the page object
        self.graph_page = GraphPage(page)
        self.graph_page.navigate_to_pipeline_sufficiency()
        self.page = page


    def test_all_graphs_load_initially(self):
        """
        Test that all four graphs load initially on the Pipeline Sufficiency dashboard.
        - Waits for all graphs to load
        - Asserts their visibility
        - Captures screenshots for visual verification
        """

        self.graph_page.wait_for_graphs_to_load()


        assert self.graph_page.are_all_graphs_visible(), "Not all graphs are visible on the page"
        
    def test_graphs_respond_to_filter_changes(self):
        """
        Test that graphs on the dashboard respond correctly when a filter is applied:
        - Capture initial graph data
        - Apply branch filter
        - Capture new graph data
        - Assert graph data has changed
        """
        self.graph_page.wait_for_graphs_to_load()

        # Data before applying filter
        initial_data = self.graph_page.get_all_graph_data()

        # Apply filter
        self.graph_page.change_filter("Secondary Branch")
        self.page.wait_for_load_state("networkidle")

        # Data after applying filter
        filtered_data = self.graph_page.get_all_graph_data()

        # Assertion
        assert self.graph_page.verify_data_changes_after_filter(
            initial_data, filtered_data
        ), "Graph data did not change after filter application"


    
    # def test_specific_graph_values(self):
    #     """
    #     Test that specific graph values match expected values.
    #     - This is a placeholder test where you can add assertions for known values
    #     - You can use data comparison or fixed expected values
    #     """
    #     self.graph_page.wait_for_graphs_to_load()
        
    #     # Example (pseudo-code, you must implement get_specific_value if needed)
    #     # value = self.graph_page.get_specific_value(
    #     #     self.graph_page.pipeline_sufficiency_container, "Main Branch"
    #     # )
    #     # assert value == "100%", "Pipeline sufficiency value is not as expected"
        
    #     # Placeholder to prevent empty test error
    #     assert True
