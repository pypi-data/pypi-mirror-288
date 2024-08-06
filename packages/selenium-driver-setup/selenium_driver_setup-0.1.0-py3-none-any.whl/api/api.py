# api.py
from utilities.decorators import (
    exception_non_stopper_decorator,
    exception_stopper_decorator
)

from utilities.element_waiters import (
    wait_for_element_present,
    wait_for_element_visible,
    wait_for_element_clickable,
    wait_for_text_to_be_present_in_element
)

from utilities.browser_actions import scroll_page
from utilities.logging_setup import setup_logging

from drivers import (
    ChromeDriverSetup,
    FirefoxDriverSetup,
    EdgeDriverSetup
)

__all__ = [
    'scroll_page',
    'exception_non_stopper_decorator',
    'exception_stopper_decorator',
    'wait_for_element_present',
    'wait_for_element_visible',
    'wait_for_element_clickable',
    'wait_for_text_to_be_present_in_element',
    'setup_logging',
    'ChromeDriverSetup',
    'FirefoxDriverSetup',
    'EdgeDriverSetup'
]
