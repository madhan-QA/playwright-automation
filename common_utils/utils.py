import logging
import os
import time

from typing import Type, Union, Tuple,List

class Utils:

    @staticmethod
    def setup_logging(log_dir='logs', log_level=logging.INFO):
       
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'automation.log')),
                logging.StreamHandler()
            ]
        )
        
        return logging.getLogger(__name__)

    @staticmethod
    def retry(max_attempts: int = 3, 
              delay: Union[int, float] = 1, 
              exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception):
       
        import time
        import functools
        
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                attempts = 0
                while attempts < max_attempts:
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        attempts += 1
                        if attempts == max_attempts:
                            raise
                        logging.warning(f"Attempt {attempts} failed: {e}. Retrying...")
                        time.sleep(delay)
            return wrapper
        return decorator
    


    

    @classmethod
    def safe_click(cls, locator, error_message: str = "Click action failed"):
   
        logger = cls.setup_logging()
        try:
            logger.info(f"Clicking element: {locator}")
            locator.click()
        except Exception as e:
            logger.error(f"{error_message}: {str(e)}")
            raise Exception(f"{error_message}: {str(e)}")

    @classmethod
    def safe_fill(cls, locator, text: str, error_message: str = "Fill action failed"):
       
        logger = cls.setup_logging()
        try:
            logger.info(f"Filling element with text: {text}")
            locator.fill(text)
        except Exception as e:
            logger.error(f"{error_message}: {str(e)}")
            raise Exception(f"{error_message}: {str(e)}")

    @classmethod
    def safe_download(cls, page, download_locator, error_message: str = "Download failed"):
        
        logger = cls.setup_logging()
        try:
            # Ensure downloads directory exists
            downloads_dir = 'downloads'
            os.makedirs(downloads_dir, exist_ok=True)
            
            logger.info(f"Triggering download: {download_locator}")
            
            # Expect and trigger download
            with page.expect_download() as download_info:
                download_locator.click()
            
            # Get the download object
            download = download_info.value
            
           # Use the original filename
            download_path = os.path.join(downloads_dir, download.suggested_filename)

            
            # Save the download
            download.save_as(download_path)
            
            logger.info(f"File downloaded successfully: {download_path}")
            return download_path
        except Exception as e:
            logger.error(f"{error_message}: {str(e)}")
            raise Exception(f"{error_message}: {str(e)}")

    @classmethod
    def find_and_click_by_xpath(cls, page, xpath: str, error_message: str = "Element not found or clickable"):
       
        logger = cls.setup_logging()
        try:
            logger.info(f"Finding and clicking element with XPath: {xpath}")
            element = page.locator(xpath)
            if not element.is_visible():
                raise Exception("Element is not visible")
            element.click()
        except Exception as e:
            logger.error(f"{error_message}: {str(e)}")
            raise Exception(f"{error_message}: {str(e)}")

    @classmethod
    def safe_navigation(cls, page, navigation_steps: List[Union[str, object]], error_message: str = "Navigation failed"):
    
        logger = cls.setup_logging()
        try:
            logger.info("Starting navigation process")
            for step in navigation_steps:
                # If step is a string (assumed to be XPath), use find_and_click_by_xpath
                if isinstance(step, str):
                    cls.find_and_click_by_xpath(page, step)
                # If step is a locator, use safe_click
                else:
                    cls.safe_click(step)
            logger.info("Navigation completed successfully")
        except Exception as e:
            logger.error(f"{error_message}: {str(e)}")
            raise Exception(f"{error_message}: {str(e)}")