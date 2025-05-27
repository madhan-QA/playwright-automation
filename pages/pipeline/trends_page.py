"""
trends page object
"""
from pages.base_page import BasePage
from playwright.sync_api import Page, expect
import time



class TrendsGraphPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
    # Element locators
        self.PIPELINE_SUFFICIENCY_BUTTON = "role=button[name='Pipeline Sufficiency']"
        self.PIPELINE_TENDS_LINK = "a:has-text('Trend')"
    

    # XPath selectors for the pipeline sufficiency grap
    # Main graph container - for visibility checks
    MAIN_GRAPH_CONTAINER = "//div[@class='growth_opportunities layout-margin layout-xs-column layout-sm-column layout-md-column layout-gt-md-row layout-align-sm-space-between-stretch layout-align-md-space-between-stretch layout-align-gt-md-space-between-stretch flex']"
    
    # Alternative shorter path for main container
    MAIN_GRAPH_CONTAINER_SHORT = "//div[contains(@class, 'growth_opportunities')]"
    
    # Graph card container - more specific
    GRAPH_CARD_CONTAINER = "//md-card[contains(@class, 'sell_out_by_brand')]"
    
    # FusionCharts container - the actual chart
    FUSIONCHARTS_CONTAINER = "//div[contains(@class, 'fusioncharts-container')]"
    
    # SVG element containing the chart
    CHART_SVG = "//svg[@id[starts-with(., 'raphael-paper')]]"
    
    # More specific chart identification
    CHART_SVG_SPECIFIC = "//span[contains(@class, 'fusioncharts-container')]//svg"
    
    # For getting data values - FusionCharts specific
    CHART_DATA_ELEMENTS = "//svg[@id[starts-with(., 'raphael-paper')]]//rect[@fill-opacity='1']"
    
    # Chart legend elements (for data extraction)
    CHART_LEGEND = "//g[contains(@class, 'raphael-group') and contains(@class, 'legend')]//text"
    
    # Tooltip elements (when hovering over chart elements)
    CHART_TOOLTIP = "//div[contains(@class, 'fc__tooltip')]"
    
    # KPI selector dropdown
    KPI_SELECTOR = "//md-select[@name='opp_progress']"
    
    # Chart loading indicator
    CHART_LOADING = "//div[@ng-show='!trendChartShow' and contains(@class, 'ng-hide')]"
    
    # Chart visible state
    CHART_VISIBLE = "//div[@ng-if='trendChartShow']"

# For your specific use case, here are the selectors to use:

pipeline_graph_containers = {
    # Main container for visibility check
    "pipeline_sufficiency_graph": "//div[contains(@class, 'growth_opportunities')]//md-card[contains(@class, 'sell_out_by_brand')]",
    
    # FusionCharts specific container
    "fusioncharts_container": "//span[contains(@class, 'fusioncharts-container')]",
    
    # SVG chart element
    "chart_svg": "//svg[@id[starts-with(., 'raphael-paper')]]",
    
    # For data extraction - chart elements
    "chart_data_elements": "//svg[@id[starts-with(., 'raphael-paper')]]//g[contains(@class, 'raphael-group')]//rect[@fill-opacity='1']",
}



# Updated methods for your class:

def are_all_graphs_visible(self):
    """Check if all graphs are visible and take element-level screenshots."""
    all_visible = True
    
    # Updated selectors
    graph_selectors = {
        "pipeline_sufficiency_main": "//div[contains(@class, 'growth_opportunities')]//md-card[contains(@class, 'sell_out_by_brand')]",
        "fusioncharts_svg": "//svg[@id[starts-with(., 'raphael-paper')]]",
        "chart_container": "//span[contains(@class, 'fusioncharts-container')]"
    }
    
    for name, selector in graph_selectors.items():
        try:
            if not self.page.is_visible(selector):
                print(f"Graph not visible: {name}")
                all_visible = False
            else:
                element = self.page.locator(selector)
                element.screenshot(path=f"reports/{name}_graph.png")
        except Exception as e:
            print(f"Error processing {name}: {e}")
            all_visible = False
    return all_visible

def get_graph_data(self, graph_selector):
    """Extract data from FusionCharts graph."""
    graph = self.page.locator(graph_selector)
    try:
        graph.wait_for(state="visible", timeout=5000)
    except Exception as e:
        self.logger.warning(f"Graph not found for selector: {graph_selector}. Error: {str(e)}")
        return {"status": "not_found", "values": []}

    # For FusionCharts, we need to extract data differently
    # Try to get data from chart elements
    try:
        # Method 1: Try to get data from SVG rect elements (chart bars/columns)
        chart_rects = graph.locator("//svg//rect[@fill-opacity='1']")
        rect_count = chart_rects.count()
        
        if rect_count > 0:
            # Extract height or other attributes that represent data
            values = []
            for i in range(rect_count):
                try:
                    rect = chart_rects.nth(i)
                    height = rect.get_attribute("height")
                    width = rect.get_attribute("width")
                    y_pos = rect.get_attribute("y")
                    values.append(f"h:{height},w:{width},y:{y_pos}")
                except Exception as e:
                    values.append("error")
            return {"status": "ok", "values": values, "type": "svg_data"}
        
        # Method 2: Try to get data from tooltip or data attributes
        data_elements = graph.locator("[data-value], [data-original-value]")
        data_count = data_elements.count()
        
        if data_count > 0:
            values = []
            for i in range(data_count):
                try:
                    element = data_elements.nth(i)
                    value = element.get_attribute("data-value") or element.get_attribute("data-original-value")
                    values.append(value or "no_value")
                except Exception:
                    values.append("error")
            return {"status": "ok", "values": values, "type": "data_attributes"}
        
        # Method 3: Check if chart is loading or has no data
        loading_indicator = self.page.locator("//div[@ng-show='!trendChartShow']")
        if loading_indicator.is_visible():
            return {"status": "loading", "values": []}
        
        return {"status": "no_data", "values": []}
        
    except Exception as e:
        self.logger.warning(f"Failed to extract data from {graph_selector}: {str(e)}")
        return {"status": "error", "values": [], "error": str(e)}

def get_all_graph_data(self):
    """Fetch data values and status from all graphs."""
    selectors = {
        "pipeline_sufficiency_chart": "//div[contains(@class, 'growth_opportunities')]//md-card[contains(@class, 'sell_out_by_brand')]",
        "fusioncharts_svg": "//svg[@id[starts-with(., 'raphael-paper')]]",
    }
    
    return {
        key: self.get_graph_data(selector)
        for key, selector in selectors.items()
    }

# Additional helper methods for FusionCharts interaction:

def wait_for_chart_to_load(self):
    """Wait for FusionCharts to fully load."""
    try:
        # Wait for the chart container to be visible
        self.page.wait_for_selector("//span[contains(@class, 'fusioncharts-container')]", timeout=10000)
        
        # Wait for SVG to be present
        self.page.wait_for_selector("//svg[@id[starts-with(., 'raphael-paper')]]", timeout=10000)
        
        # Wait for chart elements to be rendered
        self.page.wait_for_selector("//svg//rect[@fill-opacity='1']", timeout=10000)
        
        return True
    except Exception as e:
        self.logger.warning(f"Chart failed to load: {str(e)}")
        return False

def get_chart_legend_data(self):
    """Extract legend information from the chart."""
    try:
        legend_elements = self.page.locator("//g[contains(@class, 'legend')]//text")
        legend_count = legend_elements.count()
        
        legend_items = []
        for i in range(legend_count):
            try:
                text = legend_elements.nth(i).inner_text().strip()
                if text:  # Only add non-empty text
                    legend_items.append(text)
            except Exception:
                continue
                
        return legend_items
    except Exception as e:
        self.logger.warning(f"Failed to extract legend data: {str(e)}")
        return []

def interact_with_chart_element(self, element_index=0):
    """Hover over chart element to trigger tooltip."""
    try:
        chart_elements = self.page.locator("//svg//rect[@fill-opacity='1']")
        if chart_elements.count() > element_index:
            chart_elements.nth(element_index).hover()
            # Wait for tooltip to appear
            self.page.wait_for_selector("//div[contains(@class, 'fc__tooltip')]", timeout=2000)
            return True
    except Exception as e:
        self.logger.warning(f"Failed to interact with chart element: {str(e)}")
    return False
