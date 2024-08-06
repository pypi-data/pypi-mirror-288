from chrome_driver import ChromeDriverSetup
from firefox_driver import FirefoxDriverSetup
from edge_driver import EdgeDriverSetup

class DriverFactory:
    @staticmethod
    def get_driver(browser, proxy=None, headless=True):
        """
        Factory method to instantiate a web driver based on the browser type.
        
        Args:
            browser (str): The type of browser ('chrome', 'firefox', 'edge').
            proxy (str): Proxy setting for the WebDriver.
            headless (bool): Whether to run the browser in headless mode.

        Returns:
            WebDriver: An instance of a WebDriver for the specified browser.
        
        Raises:
            ValueError: If the browser type is unsupported.
        """
        if browser.lower() == 'chrome':
            return ChromeDriverSetup(proxy=proxy, headless=headless).get_driver()
        
        elif browser.lower() == 'firefox':
            return FirefoxDriverSetup(proxy=proxy, headless=headless).get_driver()
        
        elif browser.lower() == 'edge':
            return EdgeDriverSetup(proxy=proxy, headless=headless).get_driver()
        
        else:
            raise ValueError(f"Unsupported browser type: {browser}")