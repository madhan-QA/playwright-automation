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

              # Wait for network activity to complete after login
            self.logger.info("Waiting for network activity to complete")
            try:
                self.wait_for_state(state="networkidle", timeout=15000)
            except Exception as e:
                self.logger.warning(f"Network did not reach idle state: {str(e)}")
            
            # Take a screenshot to see the state after login
            time.sleep(2)

            self.logger.info("Taking screenshot after login")
            self.take_screenshot(name="post_login.png")
            


            # Check for and dismiss the dialog
            self.wait_for_state()
            if self.is_element_visible(self.CANCEL_DIALOG_BUTTON):
                self.logger.info("Release notes dialog found. Attempting to dismiss.")
                self.click_element(self.CANCEL_DIALOG_BUTTON)
            else:
                self.logger.info("Release notes dialog not present.")
          
        
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            # Take screenshot on failure
            self.page.screenshot(path="screenshots/login_failure.png")
            return False    
