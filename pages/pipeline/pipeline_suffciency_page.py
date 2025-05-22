"""
Dashboard page object
"""
from pages.base_page import BasePage
from playwright.sync_api import Page, expect
import time


    
class GraphPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Element locators
        self.PIPELINE_SUFFICIENCY_BUTTON = "role=button[name='Pipeline Sufficiency']"
        self.PIPELINE_SUFFICIENCY_LINK = "a:has-text('Pipeline Sufficiency')"
        self.PIPELINE_TENDS_LINK = "a:has-text('Trend')"


        # Centralized graph container selectors by key
        self.graph_containers = {
                "total_incremental_expected": 'xpath=//*[@id="mdCardContent"]/div[1]/div[2]/md-card[.//label[contains(text(),"Total Incremental Expected % (Against PY Actual)")]]',
                "churn_percentage": 'xpath=//*[@id="mdCardContent"]/div[1]/div[2]/md-card[2][.//label[contains(text(), "Churn % (Against PY Full Achievement)")]]',
                "cyi_new_win": 'xpath=//*[@id="mdCardContent"]/div[1]/div[3]/md-card[.//label[contains(text(),"CYI New WIN % (Against Final Net Incremental Target)")]]',
                "pipeline_sufficiency": 'xpath=//*[@id="mdCardContent"]/div[1]/div[3]/md-card[.//label[contains(text(),"Pipeline Sufficiency %")]]'
            }

        # Chart elements (optional)
        self.chart_canvas = "canvas"
        self.chart_legend = "div.legend-container"

        # Filter selectors - adjust as per actual DOM
        self.FILTERS_BUTTON = 'xpath=//*[@id="mdToolbar"]//button[.//span[contains(text(), "Filters")]]'
        self.BRANCH_FILTER = 'xpath=//md-select[@name="select_branch"]'
        self.DSR_FILTER = 'xpath=//md-select[@name="select_dsr"]'
        self.LOB_FILTER = 'xpath=//md-select[@name="lob"]'
        self.TIER_FILTER = 'xpath=//md-select[@name="Tier"]'
        self.FILTERS_SEARCH = 'xpath=//*[@id="filter_list"]//button[.//span[contains(text(), "Search")]]'



    def navigate_to_pipeline_sufficiency(self):
        """Navigate to the Pipeline Sufficiency page."""
        self.click_element(self.PIPELINE_SUFFICIENCY_BUTTON)
        self.wait_for_state()

    def wait_for_graphs_to_load(self,timeout=30000):
        for selector in self.graph_containers.values():
            self.wait_for_state(selector=selector, state="visible", timeout=timeout)
        time.sleep(3)  # Extra wait for animations or rendering


    def are_all_graphs_visible(self):
        """Check if all graphs are visible and take element-level screenshots."""
        all_visible = True
        for name, selector in self.graph_containers.items():
            try:
                if not self.page.is_visible(selector):
                    print(f"Graph not visible: {name}")
                    all_visible = False

                element = self.page.locator(selector)
                element.screenshot(path=f"reports/{name}_graph.png")
            except Exception as e:
                print(f"Error processing {name}: {e}")
                all_visible = False
        return all_visible

    def get_graph_data(self, graph_selector):
        """Extract .data-value text from a graph, safely handling missing elements."""
        graph = self.page.locator(graph_selector)
        try:
            graph.wait_for(state="visible", timeout=5000)
        except Exception as e:
            self.logger.warning(f"Graph not found for selector: {graph_selector}. Error: {str(e)}")
            return {"status": "not_found", "values": []}

        data_elements = graph.locator(".data-value")
        count = data_elements.count()
        if count == 0:
            return {"status": "no_data", "values": []}

        values = []
        for i in range(count):
            try:
                text = data_elements.nth(i).inner_text().strip()
                values.append(text)
            except Exception as e:
                self.logger.warning(f"Failed to read data-value at index {i} for {graph_selector}: {str(e)}")
                values.append("error")

        return {"status": "ok", "values": values}


    def get_all_graph_data(self):
        """Fetch data values and status from all graphs."""
        return {
            key: self.get_graph_data(selector)
            for key, selector in self.graph_containers.items()
        }


    def change_filter(self, branch=None, dsr=None, lob=None, tier=None):
        """Change a specific dashboard filter and trigger graph reload."""
        # Step 1: Click the Filters button to open the filter modal/section
        
        self.click_element(self.FILTERS_BUTTON)
 
          # Step 2: Prepare mapping of filter names to locators and values
        filters_to_apply = {
            self.BRANCH_FILTER: branch,
            self.DSR_FILTER: dsr,
            self.LOB_FILTER: lob,
            self.TIER_FILTER: tier
        }

        # Step 3: Apply each filter if a value is provided
        for locator, value in filters_to_apply.items():
            if value:
                self.logger.info(f"Attempting to set {locator} to {value}")
                success = self.select_dropdown_by_text(locator, value)
                if not success:
                    self.logger.info(f"Failed to apply filter for locator: {locator} with value: {value}")
                    return False



        # Step 5: Click the Search button to apply filters
        self.click_element(self.FILTERS_SEARCH)
        self.logger.info("Clicked Search button to apply filters")


        # Step 6: Wait for graphs to load
        self.wait_for_graphs_to_load()
        self.page.wait_for_timeout(2000)   # Optional wait for rendering

        return True


    def get_branch_value(self):
        """Return the current selected branch value."""
        branch_element = self.page.query_selector("text=Main Branch")
        return branch_element.inner_text() if branch_element else None

    def verify_data_changes_after_filter(self, before_data, after_data):
        """Check if any graph value has changed after applying a filter."""
        return any(before_data[key] != after_data[key] for key in before_data)
