"""Waits helper for Appium tests.

Provides small wrappers around selenium WebDriverWait and common
ExpectedConditions to keep page objects concise and consistent.
"""
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Waits:
    def __init__(self, driver, timeout=10, poll_frequency=0.5):
        """Create a Waits helper.

        :param driver: Appium / Selenium WebDriver instance
        :param timeout: default timeout in seconds
        :param poll_frequency: polling interval for WebDriverWait
        """
        self.driver = driver
        self.timeout = timeout
        self.poll = poll_frequency
        self.logger = logging.getLogger(self.__class__.__name__)

    def until_element(self, locator):
        """Wait until a single element is present in the DOM and return it."""
        try:
            return WebDriverWait(self.driver, self.timeout, self.poll).until(
                lambda d: d.find_element(*locator)
            )
        except Exception:
            self.logger.exception("Timeout waiting for element: %s", locator)
            raise

    def until_elements(self, locator):
        """Wait until one or more elements matching locator are present and return list."""
        try:
            return WebDriverWait(self.driver, self.timeout, self.poll).until(
                lambda d: d.find_elements(*locator)
            )
        except Exception:
            self.logger.exception("Timeout waiting for elements: %s", locator)
            raise

    def until_visible(self, locator):
        """Wait until the element is visible on screen and return it."""
        try:
            return WebDriverWait(self.driver, self.timeout, self.poll).until(
                EC.visibility_of_element_located(locator)
            )
        except Exception:
            self.logger.exception("Timeout waiting for visibility of: %s", locator)
            raise

    def until_clickable(self, locator):
        """Wait until the element is clickable and return it."""
        try:
            return WebDriverWait(self.driver, self.timeout, self.poll).until(
                EC.element_to_be_clickable(locator)
            )
        except Exception:
            self.logger.exception("Timeout waiting for clickable: %s", locator)
            raise
