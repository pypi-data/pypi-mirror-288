import time

from selenium.webdriver.remote.webdriver import WebDriver

def scroll_page(driver: WebDriver, retries: int = 5, time_sleep_scroll: int = 3) -> None:
    """
    Scrolls the page to load all the elements.
    
    Args:
        driver (WebDriver): The Selenium WebDriver instance used to interact with the web page.
        retries (int): The number of retries to attempt if the page is not fully loaded.
        time_sleep_scroll (int): The time to sleep between scrolls.
    
    """

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(time_sleep_scroll)  

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            if retries <= 0:
                break

            else:
                retries -= 1
                time.sleep(time_sleep_scroll) 

        last_height = new_height

    
    
    