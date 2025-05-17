"""
Dashboard page object
"""
from page.base_page import BasePage

class DashboardPage(BasePage):
    """Page object for dashboard page"""

    def __init__(self, page):
        """Initialize login page"""
        super().__init__(page)

    
    # Element locators
    PIPELINE_SUFFICIENCY_BUTTON = "role=button[name='Pipeline Sufficiency']"
    SALES_DASHBOARD_BUTTON = "role=button[name='Sales Dashboard']"
    REPORTS_BUTTON = "role=button[name='Reports']"
    SPANCOP_DASHBOARD_BUTTON = "role=button[name='SPANCOP Dashboard']"
    DSR_DETAILS_LINK = "a:has-text('DSR wise Details')"
    KPI_INSIGHTS_BUTTON = "role=button[name='KPI Insights']"
    KPI_TRENDS_BUTTON = "role=button[name='KPI Trends']"
    TRENDS_COMPARISON_BUTTON = "role=button[name='Trends Comparison']"
    MULTIPLE_KPIS_BUTTON="a:has-text('Multiple KPIs')"
    MULTIPLE_TIME_BUTTON="a:has-text('Multiple Time')"
    CHURN_ANALYSIS_BUTTON = "role=button[name='Churn Analysis']"
    CHURN_VS_NEW_WIN_BUTTON = "role=button[name='Churn v/s New WIN']"
    CHURN_VS_REGAINED_BUTTON = "role=button[name='Churn v/s Regained']"
    CHURN_DASHBOARD_BUTTON = "role=button[name='Churn Dashboard']"
    PROJECTED_CHURN_LINK = "a:has-text('Projected Churn')"
    SKUS_CHURN_LINK = "a:has-text('SKUs Churn')"
    XSELL_DASHBOARD_BUTTON = "role=button[name='X-Sell Dashboard']"
    PIPELINE_DASHBOARD_BUTTON = "role=button[name='Pipeline Dashboard']"
    SPANCOP_DASHBOARD_BUTTON = "role=button[name='SPANCOP Dashboard']"
    SPANCOP_MOVEMENT_DASHBOARD_BUTTON = "role=button[name='SPANCOP Movement Dashboard']"
    CPT_DASHBOARD_BUTTON = "role=button[name='CPT Dashboard']"
    DASHBOARD_VIEW_BUTTON = "role=button[name='Dashboard View']"
    PIPELINE_BUTTON = "role=button[name='Pipeline'][exact=true]"
    SALES_BUTTON = "role=button[name='Sales'][exact=true]"

    DASHBOARD_VIEW_BUTTON = "role=button[name='Dashboard View']"
    SUMMARY_LINK="a:has-text('Summary')"
    TARGET_ACHIEVMENT_BUTTON="a:has-text('Target - Achievement')"
    SELLIN_SELLOUT="a:has-text('Sell In - Sell Out')"
    CUSTOMER_VIEW_BUTTON="a:has-text('Customer View')"
    BENCHMARK_BUTTON="a:has-text('Benchmark')"
    CHRUN_CUSTOMER_LINK="a:has-text('Churn Customer')"
    PROJECTED_CUSTOMER_LINK="a:has-text('Projected Churn')"
    SKU_CHRUN_LINK="a:has-text('SKUs Churn')"
    BENCHMARK_BUTTON="a:has-text('Benchmark')"
    TRENDS_LINK = "a:has-text('Trends')"
    XSELL_LINK = "a:has-text('X-Sell')"
    NEW_WIN_LINK = "a:has-text('New Win')"
    PIPELINE_LINK = "a:has-text('Pipeline')"
    PIPELINE_SUFFICIENCY_LINK = "a:has-text('Pipeline Sufficiency')"
    PIPELINE_TENDS_LIN="role=button[name='toggle fullscreen')"




    
    def navigate_to_section(self, section_name, locator):
        """Generic navigation method that takes a section name and locator"""
        self.logger.info(f"Navigating to {section_name} using locator: {locator}")
        
        try:
            self.click_element(locator)
            self.wait_for_state()
            return True
        except Exception as e:
            self.logger.error(f"Error navigating to {section_name}: {str(e)}")
            return False
            
    