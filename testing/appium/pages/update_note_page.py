from appium.webdriver.common.appiumby import AppiumBy


class UpdateNotePage:
    TITLE_INPUT = (AppiumBy.ID, 'com.bersyte.noteapp:id/etNoteTitleUpdate')
    BODY_INPUT = (AppiumBy.ID, 'com.bersyte.noteapp:id/etNoteBodyUpdate')
    DONE_BUTTON = (AppiumBy.ID, 'com.bersyte.noteapp:id/fab_done')
    DELETE_MENU = (AppiumBy.ID, 'com.bersyte.noteapp:id/menu_delete')

    def __init__(self, driver):
        self.driver = driver

    def edit_title(self, title):
        el = self.driver.find_element(*self.TITLE_INPUT)
        el.clear()
        el.send_keys(title)

    def edit_body(self, body):
        el = self.driver.find_element(*self.BODY_INPUT)
        el.clear()
        el.send_keys(body)

    def tap_done(self):
        try:
            self.driver.find_element(*self.DONE_BUTTON).click()
        except Exception:
            # fallback to back navigation which may save
            self.driver.back()

    def tap_delete(self):
        """Tap the delete menu item to remove the current note."""
        try:
            self.driver.find_element(*self.DELETE_MENU).click()
        except Exception:
            # If menu isn't visible, try opening options menu
            try:
                self.driver.open_notifications()
            except Exception:
                pass
