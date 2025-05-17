"""
Dashboard page object
"""
from page.base_page import BasePage
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
        self.filter_dropdown = "#filter-dropdown"
        self.filter_options = ".filter-option"

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
            graph.wait_for_state(state="visible", timeout=50000)
        except:
            return ["Graph not found"]

        data_elements = graph.locator(".data-value")
        count = data_elements.count()
        if count == 0:
            return ["No data"]
        return [data_elements.nth(i).inner_text() for i in range(count)]

    def get_all_graph_data(self):
        """Fetch data values from all graphs."""
        return {
            key: self.get_graph_data(selector)
            for key, selector in self.graph_containers.items()
        }

    def change_filter(self, filter_value):
        """Change the dashboard filter and wait for graphs to reload."""
        self.click_element(self.filter_dropdown)
        self.click_element(f"{self.filter_options}:has-text('{filter_value}')")
        self.wait_for_graphs_to_load()
        time.sleep(2)  # Optional delay for graph rendering

    def get_branch_value(self):
        """Return the current selected branch value."""
        branch_element = self.page.query_selector("text=Main Branch")
        return branch_element.inner_text() if branch_element else None

    def verify_data_changes_after_filter(self, before_data, after_data):
        """Check if any graph value has changed after applying a filter."""
        return any(before_data[key] != after_data[key] for key in before_data)
