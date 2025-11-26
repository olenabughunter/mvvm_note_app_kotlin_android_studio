# NOTE: Appium's Python client implements the WebDriver protocol. We use
# selenium.webdriver.support.ui.WebDriverWait for explicit waits because they
# work against any WebDriver-compatible driver (including Appium's).
from appium.webdriver.common.appiumby import AppiumBy


class UpdateNotePage:
    TITLE_INPUT = (AppiumBy.ID, 'com.bersyte.noteapp:id/etNoteTitleUpdate')
    BODY_INPUT = (AppiumBy.ID, 'com.bersyte.noteapp:id/etNoteBodyUpdate')
    DONE_BUTTON = (AppiumBy.ID, 'com.bersyte.noteapp:id/fab_done')
    DELETE_MENU = (AppiumBy.ID, 'com.bersyte.noteapp:id/menu_delete')

    def __init__(self, driver):
        self.driver = driver

    def edit_title(self, title):
        from selenium.webdriver.support.ui import WebDriverWait

        wait = WebDriverWait(self.driver, 10)
        el = wait.until(lambda d: d.find_element(*self.TITLE_INPUT))
        el.clear()
        el.send_keys(title)

    def edit_body(self, body):
        from selenium.webdriver.support.ui import WebDriverWait

        wait = WebDriverWait(self.driver, 10)
        el = wait.until(lambda d: d.find_element(*self.BODY_INPUT))
        el.clear()
        el.send_keys(body)

    def tap_done(self):
        from selenium.webdriver.support.ui import WebDriverWait

        wait = WebDriverWait(self.driver, 5)
        try:
            el = wait.until(lambda d: d.find_element(*self.DONE_BUTTON))
            el.click()
        except Exception:
            # fallback to back navigation which may save
            self.driver.back()

    def tap_delete(self):
        """Tap the delete menu item to remove the current note."""
        from selenium.webdriver.support.ui import WebDriverWait

        wait = WebDriverWait(self.driver, 5)
        try:
            el = wait.until(lambda d: d.find_element(*self.DELETE_MENU))
            el.click()
        except Exception:
            # If menu isn't visible, try opening options menu as a last resort
            try:
                self.driver.open_notifications()
            except Exception:
                pass
