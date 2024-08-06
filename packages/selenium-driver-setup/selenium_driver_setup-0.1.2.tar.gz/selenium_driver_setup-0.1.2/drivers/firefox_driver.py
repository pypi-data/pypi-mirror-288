import logging

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException

from drivers.webdriver_setup import WebDriverSetup

class FirefoxDriverSetup(WebDriverSetup):
    def get_driver(self):
        options = FirefoxOptions()
        self.setup_options(options)  
        try:
            self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
            logging.info("Firefox WebDriver setup complete.")

        except WebDriverException as e:
            self.handle_webdriver_error(e)
            
        return self.driver
