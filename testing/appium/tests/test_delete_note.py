import time
from testing.appium.pages.home_page import HomePage
import pytest


@pytest.mark.regression
def test_delete_note_flow(driver):
    home = HomePage(driver)
    # create a new note first
    new_page = home.tap_add()
    title = f"E2E Delete Note {int(time.time())}"
    new_page.enter_title(title)
    new_page.enter_body('Body to delete')
    new_page.tap_save()

    from testing.appium.waits import Waits
    from appium.webdriver.common.appiumby import AppiumBy

    wait = Waits(driver, 10)
    wait.until_elements((AppiumBy.ID, 'com.bersyte.noteapp:id/tvNoteTitle'))
    assert home.has_note_with_title(title)

    # open first note and delete
    update_page = home.open_first_note()
    update_page.tap_delete()

    # wait and verify note no longer present
    wait.until(lambda d: not any(title in e.text for e in d.find_elements(AppiumBy.ID, 'com.bersyte.noteapp:id/tvNoteTitle')))
    assert not home.has_note_with_title(title)
