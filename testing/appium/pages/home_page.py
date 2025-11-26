from appium.webdriver.common.appiumby import AppiumBy


class HomePage:
    # resource ids from app
    ADD_BUTTON = (AppiumBy.ID, 'com.bersyte.noteapp:id/fabAddNote')
    NOTES_RECYCLER = (AppiumBy.ID, 'com.bersyte.noteapp:id/recyclerView')
    NOTE_TITLE_ITEMS = (AppiumBy.ID, 'com.bersyte.noteapp:id/tvNoteTitle')

    def __init__(self, driver):
        self.driver = driver

    def tap_add(self):
        """Tap the FAB to open the New Note screen and return the NewNotePage object."""
        from testing.appium.pages.new_note_page import NewNotePage
        self.driver.find_element(*self.ADD_BUTTON).click()
        return NewNotePage(self.driver)

    def open_first_note(self):
        """Open the first note in the list and return the UpdateNotePage object."""
        from testing.appium.pages.update_note_page import UpdateNotePage
        elems = self.driver.find_elements(*self.NOTE_TITLE_ITEMS)
        if not elems:
            raise Exception("No notes available to open")
        elems[0].click()
        return UpdateNotePage(self.driver)

    def has_note_with_title(self, title):
        # find note title elements and compare text
        elems = self.driver.find_elements(*self.NOTE_TITLE_ITEMS)
        for e in elems:
            try:
                if title in e.text:
                    return True
            except Exception:
                continue
        return False
