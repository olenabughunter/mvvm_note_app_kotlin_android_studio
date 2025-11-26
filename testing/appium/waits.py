from selenium.webdriver.support.ui import WebDriverWait


class Waits:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def until_element(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(lambda d: d.find_element(*locator))

    def until_elements(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(lambda d: d.find_elements(*locator))
