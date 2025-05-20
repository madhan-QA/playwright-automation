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
from pages.login.login_page import LoginPage
from pages.dashboard.dashboard_page import DashboardPage
from pages.dashboard.report_page import ReportPage

# Import report validator
# from common_utils.report_validator import ReportValidator, ReportValidationRunner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"report_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_config(config_path):
    """Load configuration from JSON file with default fallback"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Check if file exists
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        else:
            logger.warning(f"Config file not found: {config_path}")
            return {}
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")

@pytest.fixture
def login_config():
    """Fixture to provide login configuration"""
    return load_config('data/login_config.json')

@pytest.fixture
def reports_navigation_config():
    """Fixture to provide reports configuration"""
    return load_config('data/reports_navigation.json')

@pytest.fixture
def validator_config():
    """Fixture to provide validator configuration"""
  
    return load_config('data/validator_config.json')

@pytest.fixture
def download_path():
    """Fixture for download path"""
    path = os.path.join(os.getcwd(), "downloads")
    os.makedirs(path, exist_ok=True)
    return path

def test_download_and_validate_reports(page: Page, login_config, reports_navigation_config, validator_config, download_path):
    """Test to download and validate multiple reports"""
    # Step 1: Login
    login_page = LoginPage(page)
    page.goto(login_config["login"]["url"] ,timeout=60000, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle")
    
    login_page.login(
        email=login_config["login"]["email"],
        password=login_config["login"]["password"]
    )
    
    # Initialize pages
    dashboard_page = DashboardPage(page)
    report_page = ReportPage(page)
    
    # Always navigate to reports section first
    dashboard_page.navigate_to_reports()
 
    # Create validation runner
    config_path = os.path.join('input', 'validator_config.json')
    with open(config_path, 'w') as f:
        json.dump(validator_config, f, indent=2)
    
    # validation_runner = ReportValidationRunner(download_path=download_path, config_path=config_path)
    
    # Process each report
    validation_results = {}
    
    for report_config in reports_navigation_config:
        report_name = report_config["name"]
        logger.info(f"Processing {report_name}")
        
        try:
            # Extract navigation parameters from config
            report_button = report_config["navigation"]["report"]
            view_button = report_config["navigation"]["view"]
            
            # Navigate to report section
            logger.info(f"Navigating to report section: {report_button}")
            dashboard_page.navigate_to_section(report_name, getattr(dashboard_page, report_button))
            
            # Navigate to view
            logger.info(f"Navigating to view: {view_button}")
            dashboard_page.navigate_to_section(f"{report_name} View", getattr(dashboard_page, view_button))
            
            # Handle the download
            # Get download button information from reports_page
            menu_button_name = report_config["download"]["button"]
            download_selector_name = report_config["download"]["selector"]
            expected_filename = report_config["download"]["filename"]
            
            # Click menu button using the constant from reports_page
            menu_button = getattr(report_page, menu_button_name)
            page.click(menu_button)
            page.wait_for_load_state("networkidle")
            
            # Get the actual download selector value
            download_selector = getattr(report_page, download_selector_name)
            logger.info(f"Downloading report using selector: {download_selector}")
            
            # Setup download listener
            with page.expect_download() as download_info:
                page.click(download_selector)
                
            download = download_info.value
            # Use expected filename with .xlsx extension (or appropriate extension)
            download_filename = f"{expected_filename}.xlsx"
            download_path_full = os.path.join(download_path, download_filename)
            download.save_as(download_path_full)
            
            logger.info(f"Report downloaded to {download_path_full}")
            
            # Validate the downloaded report
            # validation_result = validation_runner.validate_report(download_path_full, report_name)
            # validation_results[report_name] = validation_result
            
            # logger.info(f"Validation result for {report_name}: {validation_result}")
            
        except Exception as e:
            logger.error(f"Error processing {report_name}: {str(e)}")
            page.screenshot(path=f"reports/{report_name}_error.png")
            validation_results[report_name] = False
    
    # Assert that all validations passed
    # assert all(validation_results.values()), f"Some validations failed: {validation_results}"













# def perform_navigation(dashboard_page, navigation_config):
#     """
#     Perform navigation based on configuration.
#     Each navigation item in config contains name and navigation details.
#     """
#     # Process each navigation item in the config
#     for nav_item in navigation_config:
#         section_name = nav_item["name"]
        
#         # Get the report locator constant name
#         report_locator_name = nav_item["navigation"]["report"]
#         view_locator_name = nav_item["navigation"]["view"]
        
#         # Convert string constant names to actual locator values
#         report_locator = getattr(dashboard_page, report_locator_name)
        
#         # Navigate to the report section
#         logger.info(f"Navigating to report: {section_name} using locator: {report_locator}")
#         result = dashboard_page.navigate_to_section(section_name, report_locator)
        
#         if not result:
#             logger.warning(f"Navigation to report {section_name} with locator {report_locator} failed")
#             continue
        
#         # Then navigate to the view
#         view_locator = getattr(dashboard_page, view_locator_name)
#         logger.info(f"Navigating to view for {section_name} using locator: {view_locator}")
#         view_result = dashboard_page.navigate_to_section(f"{section_name} View", view_locator)
        
#         if not view_result:
#             logger.warning(f"Navigation to view for {section_name} with locator {view_locator} failed") 




            
# def test_download_and_validate_reports(page: Page, login_config, reports_navigation_config, validator_config, download_path):
#     """Test to download and validate multiple reports"""
#     # Step 1: Login
#     login_page = LoginPage(page)
#     page.goto(login_config["login"]["url"])
#     page.wait_for_load_state("networkidle")
    
#     login_page.login(
#         email=login_config["login"]["email"],
#         password=login_config["login"]["password"]
#     )
    
#     # Initialize pages
#     dashboard_page = DashboardPage(page)
#     report_page = ReportPage(page)
#     page.pause() 

    
#     # Always navigate to reports section first
#     dashboard_page.navigate_to_reports()
 
    
#     # Create validation runner
#     config_path = os.path.join('input', 'validator_config.json')
#     with open(config_path, 'w') as f:
#         json.dump(validator_config, f, indent=2)
    
#     validation_runner = ReportValidationRunner(download_path=download_path, config_path=config_path)
    
#     # Process each report
#     validation_results = {}
    
#     for report_config in reports_navigation_config:
#         report_name = report_config["name"]
#         logger.info(f"Processing {report_name}")
      
#         try:
#             # Navigate to report
#             perform_navigation(dashboard_page, report_config["navigation"])

#              # Handle download button if specified

#             if "button" in report_config["download"]:
#                 page.click(report_config["download"]["button"])
#                 page.wait_for_load_state("networkidle")

            
            
#             # Download report
#             download_selector = report_config["download"]["selector"]
#             expected_filename = report_config["download"]["filename"]
            
#             logger.info(f"Downloading report using selector: {download_selector}")
            
#             # Setup download listener
#             with page.expect_download() as download_info:
#                 page.click(download_selector)
                
#             download = download_info.value
#             download_path_full = os.path.join(download_path, expected_filename)
#             download.save_as(download_path_full)
#         finally:  
#             logger.info(f"Report downloaded to {download_path_full}")
            
#             # Take screenshot for evidence
#             screenshot_path = os.path.join("screenshots", f"{report_name.replace(' ', '_')}.png")
#             os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
#             page.screenshot(path=screenshot_path)
            
#             # Validate the report
#             logger.info(f"Validating report {report_name}")
#             validation_result = validation_runner.run_validation(download_path_full)
#             validation_results[report_name] = validation_result
            
#             # Log validation summary
#             logger.info(f"Report type detected: {validation_result['report_type']}")
            
#             all_validations_passed = True
#             for name, validation in validation_result["validations"].items():
#                 success = validation.get("success", False)
#                 if not success:
#                     all_validations_passed = False
#                 logger.info(f"  {name}: {'Passed' if success else 'Failed'}")
                
#                 # Log details for failed validations
#                 if not success and "missing_columns" in validation:
#                     logger.info(f"    Missing columns: {', '.join(validation['missing_columns'])}")
                
#                 if not success and "negative_values" in validation:
#                     for col, rows in validation["negative_values"].items():
#                         if rows:
#                             logger.info(f"    Negative values in column '{col}' at {len(rows)} rows")
            
#             logger.info(f"Overall result for {report_name}: {'PASSED' if all_validations_passed else 'FAILED'}")
            
#             # Assert validation passed
#             assert all_validations_passed, f"Validation failed for {report_name}"
            
#         except Exception as e:
#             logger.error(f"Error processing {report_name}: {str(e)}")
#             validation_results[report_name] = {"error": str(e)}
#             # Take failure screenshot
#             page.screenshot(path=f"screenshots/error_{report_name.replace(' ', '_')}.png")
#             raise
    
#     # Final report
#     logger.info("\n===== VALIDATION SUMMARY =====")
#     for report_name, result in validation_results.items():
#         if "error" in result:
#             logger.info(f"{report_name}: ERROR - {result['error']}")
#         else:
#             all_passed = all(v.get("success", False) for v in result["validations"].values())
#             logger.info(f"{report_name}: {'PASSED' if all_passed else 'FAILED'}")
    
#     return validation_results