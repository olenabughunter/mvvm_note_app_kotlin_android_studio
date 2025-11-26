from appium.webdriver.common.appiumby import AppiumBy


class NewNotePage:
    TITLE_INPUT = (AppiumBy.ID, 'com.bersyte.noteapp:id/etNoteTitle')
    BODY_INPUT = (AppiumBy.ID, 'com.bersyte.noteapp:id/etNoteBody')
    SAVE_MENU = (AppiumBy.ID, 'com.bersyte.noteapp:id/menu_save')

    def __init__(self, driver):
        self.driver = driver

    def enter_title(self, title):
        el = self.driver.find_element(*self.TITLE_INPUT)
        el.clear()
        el.send_keys(title)

    def enter_body(self, body):
        el = self.driver.find_element(*self.BODY_INPUT)
        el.clear()
        el.send_keys(body)

    def tap_save(self):
        # menu item uses android menu id; sometimes accessible via resource id
        try:
            self.driver.find_element(*self.SAVE_MENU).click()
        except Exception:
            # fallback: press back to trigger save if app behaves that way
            self.driver.back()
