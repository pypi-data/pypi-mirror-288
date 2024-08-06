import logging 

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

from drivers.webdriver_setup import WebDriverSetup

class ChromeDriverSetup(WebDriverSetup):
    def get_driver(self):

        options = ChromeOptions()
        self.setup_options(options) 

        try:
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            logging.info("Chrome WebDriver setup complete.")

        except WebDriverException as e:
            self.handle_webdriver_error(e)

        return self.driver
