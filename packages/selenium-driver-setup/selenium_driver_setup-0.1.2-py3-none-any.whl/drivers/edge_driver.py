import logging

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions

from drivers.webdriver_setup import WebDriverSetup

class EdgeDriverSetup(WebDriverSetup):
    def get_driver(self):

        options = EdgeOptions()
        self.setup_options(options)  

        try:
            self.driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=options)
            logging.info("Edge WebDriver setup complete.")

        except WebDriverException as e:
            self.handle_webdriver_error(e)

        return self.driver