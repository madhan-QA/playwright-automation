import pytest
import json
import os
from playwright.sync_api import Page, expect

# Import page objects - adjust import paths based on your structure
from page.login_page import LoginPage
from page.dashboard_page import DashboardPage
from page.report_page import ReportPage

def load_config(config_path='input/login_config.json'):
    """Load test configuration"""
    try:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
    except Exception as e:
        # If config file not found, use default values
        print(f"Warning: Could not load config: {str(e)}")
        

@pytest.fixture
def test_config():
    """Fixture to provide test configuration"""
    return load_config()

# def test_login_and_download_report(page: Page, test_config):
#     """Test login and report download"""
#     # Step 1: Login
#     login_page = LoginPage(page)
#     page.goto(test_config["login"]["url"])
#     page.wait_for_load_state("networkidle")
    
#     login_page.login(
#         email=test_config["login"]["email"],
#         password=test_config["login"]["password"]
#     )
    
    # #Verify login successful
    
    # #Step 2: Navigate to reports
    # dashboard_page = DashboardPage(page)
    # dashboard_page.navigate_to_sales_dashboard()
    # dashboard_page.navigate_to_reports()
    # dashboard_page.navigate_to_spancop_dashboard()
    # dashboard_page.open_dashboard_view()
    # dashboard_page.open_dsr_details()
    
    # # Step 3: Download report
    # # report_page = ReportPage(page)
    # # download_path = report_page.download_report()
    
    # # # Verify download successful
    # # assert os.path.exists(download_path), f"Downloaded file not found at {download_path}"
    # # assert os.path.getsize(download_path) > 0, "Downloaded file is empty"
    
    # # # Take a screenshot for reporting
    # # page.screenshot(path="screenshots/download_report_success.png")


def test_example(page: Page) -> None:
    page.goto("https://shell3.isteer.co/v8_3/pm.html?#/login")
    page.get_by_role("textbox", name="Email *").click()
    page.get_by_role("textbox", name="Email *").fill("dsm_turkey@shell.com")
    page.get_by_role("textbox", name="Password *").click()
    page.get_by_role("textbox", name="Password *").fill("Amshuhu@12")
    page.get_by_role("button", name="Log in").click()
    page.get_by_text("2025 - Release 2 Skip Check").click()
    page.get_by_role("button", name="Cancel Dialog").click()
   
    page.get_by_role("button", name="Reports").click()
    page.get_by_role("button", name="Churn Analysis").click()
    page.get_by_role("button", name="Churn Dashboard").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    page.get_by_role("button", name="Download", exact=True).click()
    page.locator("a").filter(has_text="Projected Churn").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    page.get_by_role("button", name="Download", exact=True).click()
    page.locator("a").filter(has_text="SKUs Churn").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Download", exact=True).click()
    download = download_info.value
    with page.expect_download() as download2_info:
        page.get_by_role("button", name="X-Sell Dashboard").click()
    download2 = download2_info.value
    page.get_by_role("button", name="X-Sell Dashboard Real time").click()
    page.locator("a").filter(has_text="X-Sell").click()
    page.get_by_role("button", name="menu", exact=True).click()
    with page.expect_download() as download3_info:
        page.get_by_role("button", name="Download").nth(1).click()
    download3 = download3_info.value
    page.locator("a").filter(has_text="Trends").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    with page.expect_download() as download4_info:
        page.get_by_role("button", name="Download").nth(1).click()
    download4 = download4_info.value
    page.get_by_role("button", name="Pipeline Dashboard").click()
    page.locator("a").filter(has_text="New Win").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    page.get_by_role("button", name="Download", exact=True).click()
    with page.expect_download() as download5_info:
        with page.expect_popup() as page1_info:
            page.locator("#mdToolbar a").filter(has_text="Pipeline").click()
        page1 = page1_info.value
    download5 = download5_info.value
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    with page.expect_download() as download6_info:
        with page.expect_popup() as page2_info:
            page.get_by_role("button", name="Download", exact=True).click()
        page2 = page2_info.value
    download6 = download6_info.value
    page.get_by_role("button", name="SPANCOP Dashboard").click()
    page.locator("a").filter(has_text="Summary").click()
    page.get_by_role("button", name="menu", exact=True).click()
    with page.expect_download() as download7_info:
        page.get_by_role("button", name="Download").nth(1).click()
    download7 = download7_info.value
    page.get_by_role("button", name="Filters Summary DSR wise").click()
    page.locator("a").filter(has_text="DSR wise Details").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    with page.expect_download() as download8_info:
        page.get_by_role("button", name="Download").nth(1).click()
    download8 = download8_info.value
    page.get_by_role("button", name="SPANCOP Movement Dashboard").click()
    page.get_by_role("button", name="menu", exact=True).click()
    with page.expect_download() as download9_info:
        page.get_by_role("button", name="Download").nth(1).click()
    download9 = download9_info.value
    page.get_by_role("button", name="CPT Dashboard").click()
    page.locator("a").filter(has_text="Summary").click()
    page.get_by_role("button", name="menu", exact=True).click()
    page.get_by_role("button", name="Download").nth(1).click()
    page.locator("a").filter(has_text="DSR wise Details").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    page.get_by_role("button", name="Download").nth(1).click()
    page.get_by_role("button", name="Dashboard View").click()
    page.get_by_role("button", name="Sales", exact=True).click()
    page.get_by_role("button", name="Pipeline", exact=True).click()
    page.locator("a").filter(has_text="Summary").click()
    page.locator("a").filter(has_text="DSR wise Details").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    with page.expect_download() as download10_info:
        page.get_by_role("button", name="Download").nth(1).click()
    download10 = download10_info.value
    page.get_by_role("button", name="Filters 24-Apr-2025 Filters").click()
    page.locator("a").filter(has_text="Summary").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    with page.expect_download() as download12_info:
        page.get_by_role("button", name="Download").nth(1).click()
    download12 = download12_info.value
    page.get_by_role("button", name="Sales", exact=True).click()
    page.locator("a").filter(has_text="Summary").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    with page.expect_download() as download13_info:
        page.get_by_role("button", name="Download").nth(1).click()
    download13 = download13_info.value
    page.get_by_role("button", name="Filters Summary DSR wise").click()
    page.locator("a").filter(has_text="DSR wise Details").click()
    with page.expect_download() as download14_info:
        page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    download14 = download14_info.value
    page.get_by_role("button", name="Download").nth(1).click()
    page.get_by_role("button", name="Churn Analysis").click()
    page.get_by_role("button", name="Churn v/s New WIN").click()
    page.get_by_role("button", name="menu", exact=True).click()
    with page.expect_download() as download15_info:
        page.get_by_role("menuitem", name="Download").first.click()
    download15 = download15_info.value
    page.get_by_role("button", name="Churn v/s Regained").click()
    page.locator("a").filter(has_text="Summary").click()
    page.get_by_role("button", name="menu", exact=True).click()
    with page.expect_download() as download16_info:
        page.get_by_role("button", name="Download", exact=True).click()
    download16 = download16_info.value
    page.get_by_role("button", name="Filters Summary DSR wise").click()
    page.locator("a").filter(has_text="DSR wise Details").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    with page.expect_download() as download17_info:
        page.get_by_role("button", name="Download", exact=True).click()
    download17 = download17_info.value
    page.get_by_role("button", name="Sales Dashboard").click()
    page.locator("a").filter(has_text="Target - Achievement").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    page.get_by_role("button", name="Download Target vs Achievement as XLS", exact=True).click()
    page.locator("a").filter(has_text="Sell In - Sell Out").click()
    with page.expect_download() as download18_info:
        page.get_by_role("button", name="Filters 2025 » Month »").click()
    download18 = download18_info.value
    page.get_by_role("button", name="Filters 2025 » Month »").click()
    page.get_by_role("button", name="menu", exact=True).click()
    page.get_by_role("button", name="Download Target vs Achievement as XLS", exact=True).click()
    with page.expect_download() as download19_info:
        page.locator("a").filter(has_text="Customer View").click()
    download19 = download19_info.value
    page.get_by_role("button", name="Filters 2025 » Month »").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    with page.expect_download() as download20_info:
        page.get_by_role("button", name="Download Target vs Achievement as XLS", exact=True).click()
    download20 = download20_info.value
    page.get_by_role("button", name="Filters 2025 » Month »").click()
    page.locator("a").filter(has_text="Benchmark").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    page.get_by_role("button", name="menu", exact=True).locator("md-icon").click()
    with page.expect_download() as download21_info:
        page.get_by_role("button", name="Download Target vs Achievement as XLS", exact=True).click()
    download21 = download21_info.value
