import time
from testing.appium.pages.home_page import HomePage
import pytest


@pytest.mark.regression
def test_edit_note_flow(driver):
    home = HomePage(driver)
    # create a new note first
    new_page = home.tap_add()
    original_title = f"E2E Edit Note {int(time.time())}"
    new_page.enter_title(original_title)
    new_page.enter_body('Original body')
    new_page.tap_save()

    # wait for note to appear in list
    from selenium.webdriver.support.ui import WebDriverWait
    from appium.webdriver.common.appiumby import AppiumBy

    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: any(original_title in e.text for e in d.find_elements(AppiumBy.ID, 'com.bersyte.noteapp:id/tvNoteTitle')))
    assert home.has_note_with_title(original_title)

    # open the first note (should be the one we just created)
    update_page = home.open_first_note()
    updated_title = original_title + ' - edited'
    update_page.edit_title(updated_title)
    update_page.edit_body('Updated body')
    update_page.tap_done()

    # wait and verify updated title present
    wait.until(lambda d: any(updated_title in e.text for e in d.find_elements(AppiumBy.ID, 'com.bersyte.noteapp:id/tvNoteTitle')))
    assert home.has_note_with_title(updated_title)
