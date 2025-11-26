import time
from testing.appium.pages.home_page import HomePage
import pytest


@pytest.mark.smoke
def test_create_note_smoke(driver):
    home = HomePage(driver)
    # open New Note screen using page object
    new_note = home.tap_add()
    title = f"E2E Note {int(time.time())}"
    new_note.enter_title(title)
    new_note.enter_body('This is a test note')
    new_note.tap_save()
    # wait for note to appear in list
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from appium.webdriver.common.appiumby import AppiumBy

    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: any(title in e.text for e in d.find_elements(AppiumBy.ID, 'com.bersyte.noteapp:id/tvNoteTitle')))
    assert home.has_note_with_title(title)
