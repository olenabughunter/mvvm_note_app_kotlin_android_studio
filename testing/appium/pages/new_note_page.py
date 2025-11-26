# NOTE: Appium's Python client implements the WebDriver protocol. We use
# selenium.webdriver.support.ui.WebDriverWait (via testing.appium.waits.Waits)
# for explicit waits because they work against any WebDriver-compatible driver
# (including Appium's). Locators use AppiumBy for mobile-specific strategies.
from appium.webdriver.common.appiumby import AppiumBy
from testing.appium.waits import Waits


class NewNotePage:
    TITLE_INPUT = (AppiumBy.ID, 'com.bersyte.noteapp:id/etNoteTitle')
    BODY_INPUT = (AppiumBy.ID, 'com.bersyte.noteapp:id/etNoteBody')
    SAVE_MENU = (AppiumBy.ID, 'com.bersyte.noteapp:id/menu_save')

    def __init__(self, driver):
        self.driver = driver

    def enter_title(self, title):
        wait = Waits(self.driver, 10)
        el = wait.until_element(self.TITLE_INPUT)
        el.clear()
        el.send_keys(title)

    def enter_body(self, body):
        wait = Waits(self.driver, 10)
        el = wait.until_element(self.BODY_INPUT)
        el.clear()
        el.send_keys(body)

    def tap_save(self):
        # menu item uses android menu id; sometimes accessible via resource id
        wait = Waits(self.driver, 5)
        try:
            el = wait.until_element(self.SAVE_MENU)
            el.click()
        except Exception:
            # fallback: press back to trigger save if app behaves that way
            self.driver.back()
