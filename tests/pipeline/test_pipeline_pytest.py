# test_pipeline_pytest.py

import pytest
from playwright.sync_api import Page

# Import the page objects
from pages.pipeline.pipeline_suffciency_page import GraphPage

# Import filter data accessor (or import from conftest if moved there)
from conftest import get_filters_data


@pytest.fixture(scope="function")
def graph_page(authenticated_page) -> GraphPage:  
    """
    Creates a GraphPage instance using the authenticated page.
    Navigates to the pipeline sufficiency page once per test.
    """
    page = authenticated_page
    graph_page = GraphPage(page)
    
    # Navigate to the pipeline page
    graph_page.navigate_to_pipeline_sufficiency()
    graph_page.wait_for_graphs_to_load()
    
    # Return the graph page object
    return graph_page


class TestGraphPage:
    """
    Test class for Pipeline Sufficiency dashboard.
    Uses session-scoped authentication for efficiency.
    """

    def test_all_graphs_load_initially(self, graph_page:GraphPage):
        """
        Test that all graphs load initially on the Pipeline Sufficiency dashboard.
        """
        graph_page.wait_for_graphs_to_load()
        assert graph_page.are_all_graphs_visible(), "Not all graphs are visible on the page"

    @pytest.mark.parametrize("filters", get_filters_data())
    def test_graphs_respond_to_filter_changes(self, graph_page:GraphPage, authenticated_page, filters):
        """
        Test that graphs respond correctly when filters are applied.
        Uses the session-scoped authenticated page for all filter combinations.
        """
        # Skip if no filters data
        if not filters:
            pytest.skip("No filter data available or empty filter")
        
        # Wait for graphs to load
        graph_page.wait_for_graphs_to_load()
        
        # Capture initial data
        initial_data = graph_page.get_all_graph_data()
        
        # Apply filters
        filter_success = graph_page.change_filter(**filters)
        assert filter_success, f"Failed to apply filters: {filters}"
        
        # Wait for changes to take effect
        authenticated_page.wait_for_load_state("networkidle")
        
        # Verify all graphs are still visible
        assert graph_page.are_all_graphs_visible(), "Not all graphs are visible after filtering"
        
        # Capture data after filtering
        filtered_data = graph_page.get_all_graph_data()
        
        # Verify data changed
        assert graph_page.verify_data_changes_after_filter(
            initial_data, filtered_data
        ), f"Graph data did not change after applying filters: {filters}"


   