import os
from common_utils.utils import Utils

import logging
import time


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, page):
        """Initialize with Playwright page"""
        self.page = page
        self.logger = self._setup_logging()
    
    def _setup_logging(self):
        """Set up logging for page actions"""
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Configure logging
        logger = logging.getLogger(f"{self.__class__.__name__}")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            # Create file handler
            file_handler = logging.FileHandler("logs/automation.log")
            file_handler.setLevel(logging.INFO)
            
            # Create formatter and add to handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            
            # Add handler to logger
            logger.addHandler(file_handler)
        
        return logger
    
    def navigate(self, url):
        """Navigate to URL"""
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
    
    def get_title(self):
        """Get page title"""
        title = self.page.title()
        self.logger.info(f"Page title: {title}")
        return title
    
    def click_element(self, locator, timeout=30000):
        """Click an element with logging and error handling"""
        try:
            self.logger.info(f"Clicking element: {locator}")
            self.page.locator(locator).click(timeout=timeout)
            return True
        except Exception as e:
            self.logger.error(f"Error clicking element {locator}: {str(e)}")
            return False
    
    def fill_field(self, locator, text, timeout=10000):
        """Fill a field with logging and error handling"""
        try:
            self.logger.info(f"Filling field {locator} with text: {text}")
            self.page.locator(locator).fill(text, timeout=timeout)
            return True
        except Exception as e:
            self.logger.error(f"Error filling field {locator}: {str(e)}")
            return False
    
    def is_element_visible(self, locator, timeout=5000):
        """Check if element is visible"""
        try:
            return self.page.locator(locator).is_visible(timeout=timeout)
        except Exception:
            return False
    
    def wait_for_state(self,selector=None,state="networkidle", timeout=10000):
        """
        Wait for either page load state or element state.
        
        - If `selector` is None → wait for page load (like 'networkidle')
        - If `selector` is provided → wait for element state (like 'visible', 'attached', etc.)
        """
        if selector:
            self.logger.info(f"Waiting for element '{selector}' to be in state '{state}'")
            try:
                self.page.locator(selector).wait_for(state=state, timeout=timeout)
            except Exception as e:
                self.logger.error(f"Element '{selector}' not {state} in time: {str(e)}")
                raise
        else:
            self.logger.info(f"Waiting for page load state '{state}'")
            try:
                self.page.wait_for_load_state(state=state, timeout=timeout)
            except Exception as e:
                self.logger.error(f"Page did not reach load state '{state}' in time: {str(e)}")
                raise

    def wait_for_element(self, locator, timeout=10000):
        """Wait for an element to be visible"""
        self.logger.info(f"Waiting for element to be visible: {locator}")
        try:
            self.page.locator(locator).wait_for(state="visible", timeout=timeout)
            return True
        except Exception as e:
            self.logger.error(f"Element {locator} not visible in time: {str(e)}")
            return False    
        
    def get_text(self, locator, timeout=10000):
        """Get text content of an element"""
        try:
            self.logger.info(f"Getting text from: {locator}")
            return self.page.locator(locator).text_content(timeout=timeout)
        except Exception as e:
            self.logger.error(f"Failed to get text from {locator}: {str(e)}")
            return None    
        
    def page_refresh(self,state="networkidle",timeout=10000):

        try:
            self.logger.info("refreshing the page")
            self.page.reload()
            self.logger.info(f"waiting for page state {state}")
            self.wait_for_state(state=state,timeout=timeout)
            self.logger.info("page is refeshed")
        except Exception as e:
            self.logger.error(f"Error while refreshing page: {str(e)}")
            raise

            


    def is_element_present(self, locator, timeout=10000):
        """Check if element exists in the DOM"""
        try:
            self.page.locator(locator).wait_for(timeout=timeout)
            return True
        except Exception:
            return False


    def scroll_into_view(self, locator):
        """Scroll an element into view"""
        self.logger.info(f"Scrolling to element: {locator}")
        try:
            self.page.locator(locator).scroll_into_view_if_needed()
            return True
        except Exception as e:
            self.logger.error(f"Error scrolling to {locator}: {str(e)}")
            return False
        
    def select_dropdown_by_text(self, locator, option_text):
        """Select an option from an AngularJS Material md-select dropdown"""
        try:
            # Step 1: Click the select dropdown
            dropdown = self.page.locator(locator)
            dropdown.wait_for(state="visible", timeout=5000)
            dropdown.click(force=True)
            self.page.wait_for_timeout(300)

            
            # Step 2: Filter only visible 'md-option's with the exact text
            option_xpath = f'//div[contains(@class, "md-select-menu-container")]//md-option[.//div[normalize-space(text())="{option_text}"] or normalize-space(text())="{option_text}"]'
            option_locator = self.page.locator(option_xpath)
            option_locator.first.wait_for(state="visible", timeout=5000)

            # Optional: Log found matching options
            count = option_locator.count()
            self.logger.info(f"Found {count} visible options with text '{option_text}'")

            if count == 0:
                self.logger.info(f"Option '{option_text}' not found or is hidden.")
                return False

            # Step 4: Click the first matching visible option
            option_locator.first.click(force=True)
            return True

        except Exception as e:
            self.logger.info(f"Failed to select '{option_text}' from {locator}: {str(e)}")
            return False
 
    def upload_file(self, locator, file_path):
        """Upload a file to an input[type='file']"""
        try:
            self.logger.info(f"Uploading file {file_path} to: {locator}")
            self.page.locator(locator).set_input_files(file_path)
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload file to {locator}: {str(e)}")
            return False  
        
    def take_screenshot(self, name="screenshot"):
            """Take a screenshot of the current page"""
            path = f"screenshot/{name}.png"
            self.logger.info(f"Taking screenshot: {path}")
            self.page.screenshot(path=path)  

    def scroll_if_not_visible_then_click(self, locator):
        element = self.page.locator(locator)

        # Wait until attached
        element.wait_for(state="attached", timeout=5000)

        # Check if element is off-screen
        is_off_screen = element.evaluate(
            """el => {
                const rect = el.getBoundingClientRect();
                return rect.bottom <= 0 || rect.top >= window.innerHeight;
            }"""
        )

        if is_off_screen:
            # Scroll up slightly — this assumes vertical scroll
            self.page.mouse.wheel(0, -500)
            self.page.wait_for_timeout(1500)  # Wait 1.5 seconds for scroll to settle

        # Then use your existing safe click method
        self.click_element(self.locator)    

