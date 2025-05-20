"""
Report page object
"""
import os
from common_utils.utils import Utils

from pages.base_page import BasePage



class ReportPage(BasePage):
    """Page object for report page"""
    
    # Element locators
    MENU_BUTTON = "role=button[name='menu'] >> md-icon"
    XLS_DOWNLOAD_BUTTON = "xpath=//button[@ng-click=\"downloadFile('excel')\"]"
    DOWNLOAD_EXCEL_BUTTON = "role=button[name='Download']"
    COMBINED_DOWNLOAD_BUTTON = (
    "xpath=//button[@ng-click=\"downloadFile('excel')\"] | //button[normalize-space()='Download']"
)
    PDF_DOWNLOAD_BUTTON = "role=button[name='Download'] >> nth=2"
    
   
    
    def download_report(self):
        """Download report and return file path"""
        self.logger.info("Downloading report")
        
        try:
            # Click menu button
            self.click_element(self.MENU_BUTTON)
            
           # Use utility method to handle the download
            # Pass the locator object to safe_download
            download_path = Utils.safe_download(
                self.page,
                self.page.locator(self.XLS_DOWNLOAD_BUTTON),
                "Report download failed"
            )
            
            return download_path
        except Exception as e:
            self.logger.error(f"Download failed: {str(e)}")
            # Take screenshot on failure
            self.page.screenshot(path="screenshots/download_failure.png")
            raise Exception(f"Download failed: {str(e)}")
