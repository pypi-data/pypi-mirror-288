from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


@staticmethod
def wait_for_element_present(driver, locator, timeout=10):
    """Wait for an element to be present in the DOM."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element
    except TimeoutException:
        return None

@staticmethod
def wait_for_element_visible(driver, locator, timeout=10):
    """Wait for an element to be visible and renderable on the page."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except TimeoutException:
        return None

@staticmethod
def wait_for_element_clickable(driver, locator, timeout=10):
    """Wait for an element to be clickable."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    except TimeoutException:
        return None

@staticmethod
def wait_for_text_to_be_present_in_element(driver, locator, text, timeout=10):
    """Wait for a specific text to be present in a given element."""
    try:
        result = WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
        return result
    except TimeoutException:
        return False
