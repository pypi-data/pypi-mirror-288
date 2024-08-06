import sys
import logging
from abc import ABC, abstractmethod
from selenium.webdriver.common.options import BaseOptions

class WebDriverSetup(ABC):
    def __init__(self, proxy=None, headless=True):
        self.proxy = proxy
        self.headless = headless
        logging.basicConfig(level=logging.INFO, filename='scraper.log', filemode='a',
                            format='%(asctime)s - %(levelname)s - %(message)s')

    @abstractmethod
    def get_driver(self):
        """Abstract method to initialize the WebDriver configured with specified options."""
        pass

    def setup_options(self, options: BaseOptions):
        """ Configure common options used by all browsers. """
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-gpu")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        if self.proxy:
            options.add_argument(f"--proxy-server={self.proxy}")
        if self.headless:
            options.add_argument("--headless")
        options.add_argument(f"--user-agent={self.get_user_agent()}")

    @staticmethod
    def get_user_agent():
        """Placeholder for user-agent retrieval logic."""
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

    def handle_webdriver_error(self, error):
        """Handle errors during WebDriver initialization."""
        logging.error(f"WebDriver setup failed: {error}")
        sys.exit(1)
