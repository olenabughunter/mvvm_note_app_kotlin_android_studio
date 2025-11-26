Title: test(appium): add Waits helper and refactor POMs; document WebDriverWait usage

Summary
- Adds a small Waits helper at testing/appium/waits.py to centralize explicit wait logic.
- Refactors Page Object Models to use the Waits helper: testing/appium/pages/{new_note_page.py, home_page.py, update_note_page.py}.
- Updates Appium pytest tests to use the Waits helper: testing/appium/tests/{test_smoke_create_note.py, test_edit_note.py, test_delete_note.py}.
- Adds testing/appium/README_AUTOMATION.md explaining why selenium.webdriver.support utilities are appropriate with Appium.
- Updates testing/docs/AUTOMATION_INSTRUCTIONS.md to reference the Waits helper and README.

What I changed (high level)
- New helper: testing/appium/waits.py
- POMs now import and use Waits(driver, timeout) instead of repeating WebDriverWait calls.
- Tests use Waits to wait for elements instead of inline WebDriverWait lambdas.
- No production (app/src/main) files were modified.

Testing done here
- Static edits, refactors and basic syntax checks committed and pushed to branch: feat/appium-tests
- I did not run the Appium tests here (requires emulator + Appium server).

How to review
- Verify POM changes preserve original behavior and locators.
- Confirm timeouts (default 10s) are acceptable; suggest reducing in quick CI smoke runs.
- Ensure no production app files were changed (only files under testing/ and testing/docs/ were modified).

How to run locally (recommended)
1. Build APK: ./gradlew assembleDebug
2. Start emulator: emulator -avd <AVD_NAME> -no-window &
3. Start Appium server: appium &
4. Install requirements: cd testing/appium && pip install -r requirements.txt
5. Run tests: pytest testing/appium/tests -q

Commands to create PR locally (if you have gh CLI installed):

gh pr create --base main --head olenabughunter:feat/appium-tests \
  --title "test(appium): add Waits helper and refactor POMs; explain WebDriverWait usage" \
  --body "See PR_BODY.md in the branch for details. Changes centralize wait logic and improve test stability."

