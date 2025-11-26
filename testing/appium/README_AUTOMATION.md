Why selenium.webdriver support utilities are used with Appium

Short answer
Appium implements the WebDriver protocol and the Appium Python client builds on top of the Selenium WebDriver APIs. That means it's normal and correct to use Selenium support utilities such as WebDriverWait and expected_conditions in Appium tests. The Appium client provides the mobile driver (appium.webdriver.Remote) and mobile locators (AppiumBy); selenium's wait helpers remain the recommended, stable way to write explicit waits.

Details
- Appium is a server that speaks the WebDriver wire protocol; the Python client exposes a driver compatible with Selenium's API. You interact with the app through an Appium Remote WebDriver instance.
- selenium.webdriver.support.ui.WebDriverWait and selenium.webdriver.support.expected_conditions are generic waiting utilities that work with any WebDriver-compatible driver (including Appium's). They are used to write concise, readable explicit waits instead of time.sleep.
- For locators we use appium.webdriver.common.appiumby.AppiumBy (already used in the POMs). AppiumBy is Appium's extension for mobile-specific locator strategies.
- Newer Appium clients provide "Options" helper classes (e.g. appium.options.android.AndroidOptions) for session creation; that doesn't change the recommendation to keep using WebDriverWait.

Recommendations and next steps
- Keep WebDriverWait usage (it's correct). If desired, add a top-of-file comment in POMs explaining this relationship.
- If you prefer explicit, project-wide primitives, we can add a small helper (testing/appium/waits.py) that wraps waiting logic to keep POMs cleaner.

Planned changes (todo)
- [x] Explain why selenium support is used with Appium (this file)
- [ ] Add clarifying comments to POM files (home_page.py, new_note_page.py, update_note_page.py)
- [ ] Optionally add a small wait helper module and refactor POMs to use it
- [ ] Update automation docs to mention this detail

If you want I can add the clarifying comments to the POM files now or create the helper module — tell me which and I'll make the change.
