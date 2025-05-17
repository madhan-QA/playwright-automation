"""
Login page object
"""

import time

from page.base_page import BasePage

class LoginPage(BasePage):
    """Page object for login page"""
    
    # Element locators
    EMAIL_INPUT = "role=textbox[name='Email *']"
    PASSWORD_INPUT = "role=textbox[name='Password *']"
    LOGIN_BUTTON = "role=button[name='Log in']"
    CANCEL_DIALOG_BUTTON = "div[role='button'][aria-label='Cancel Dialog']"
    FEATURES_CARD="//label[text()='Check Out For New Features']"


    
    def __init__(self, page):
        """Initialize login page"""
        super().__init__(page)
    
    def login(self, email, password):
        """Perform login with provided credentials"""
        self.logger.info(f"Logging in with email: {email}")
        
        try:
            # Enter email
            self.click_element(self.EMAIL_INPUT)
            self.fill_field(self.EMAIL_INPUT, email)
            
            # Enter password
            self.click_element(self.PASSWORD_INPUT)
            self.fill_field(self.PASSWORD_INPUT, password)
            
            # Click inputs container (as in original script)
            self.page.locator("#inputs").click()
            
            # Click login button
            self.click_element(self.LOGIN_BUTTON)

            
            # Wait for navigation to complete
            self.wait_for_dashboard_and_dismiss_release_notes()

        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            # Take screenshot on failure
            self.page.screenshot(path="screenshots/login_failure.png")
            return False    


    def wait_for_dashboard_and_dismiss_release_notes(self, expected_url_keyword="dashboard", timeout=10000):
        """
        Waits for navigation to dashboard and dismisses the release notes dialog if present.
        
        Args:
            expected_url_keyword (str): Keyword to check in the URL (default: 'dashboard')
            timeout (int): Maximum wait time in seconds
        """
        self.logger.info("Waiting for dashboard page to load...")

        # Wait up to `timeout` seconds for expected URL
        current_url = ""
        for _ in range(timeout):
            current_url = self.page.url
            if expected_url_keyword in current_url:
                break
            time.sleep(1)

        self.logger.info(f"Final URL after login: {current_url}")

        # Check if dashboard loaded
        if expected_url_keyword in current_url:
            self.logger.info("User successfully navigated to dashboard.")

            if self.is_element_visible(self.CANCEL_DIALOG_BUTTON, timeout=5000):
                self.logger.info("Release notes dialog found. Attempting to dismiss.")
                self.click_element(self.CANCEL_DIALOG_BUTTON)
            else:
                self.logger.info("Release notes dialog not present.")
        else:
            self.logger.warning(f"User is not on the expected '{expected_url_keyword}' page.")
    
        


        
