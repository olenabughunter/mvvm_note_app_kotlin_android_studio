Automation Engineer Instructions
For: mvvm_note_app_kotlin_android_studio
Author: Test Manager (7+ years - mobile & web testing, automation)
Audience: Test Automation Engineers

IMPORTANT RULE (READ FIRST)
- Testers and automation engineers MUST NOT modify production application source code under app/src/main. All test-related code, helpers, mocks and test-only build variants must live in test source folders (app/src/test, app/src/androidTest) or in the external test project under /testing. Any request to add hooks to production code must be discussed and implemented as test-only modules by devs with clear approvals.

Repository layout (relevant paths)
- app/                      -> Android app (production + instrumented tests)
  - src/test                -> JVM unit tests (JUnit, MockK)
  - src/androidTest         -> Espresso instrumentation tests
- testing/appium/           -> External Appium test project (Python)
  - config/                 -> desired capabilities and environment config
  - pages/                  -> Page Objects (POM)
  - tests/                  -> pytest test suites
  - fixtures/               -> test data fixtures
  - conftest.py             -> Pytest fixtures & hooks

Quick-start (local)
1. Prepare environment
- Install Android SDK, Platform Tools, and required AVD images (x86_64). Ensure adb and emulator are on PATH.
- Install JDK 11 and ensure JAVA_HOME is set.

2. Build debug APK
- From repo root:
  export JAVA_HOME=$(/usr/libexec/java_home -v 11)
  ./gradlew assembleDebug
- APK path: app/build/outputs/apk/debug/app-debug.apk

3. Run instrumentation tests (optional smoke)
- Start emulator (or connect device): emulator -avd <AVD_NAME>
- Run via Gradle:
  ./gradlew connectedAndroidTest

4. Run Appium E2E tests (Python example)
- Install python deps:
  cd testing/appium
  pip install -r requirements.txt
- Start Appium server (locally or CI-managed). Example using npm Appium installation:
  appium
- Run tests with pytest:
  pytest -q testing/appium/tests
- Run a single test:
  pytest -q testing/appium/tests/test_smoke_create_note.py::test_create_note

Design & development guidelines for tests
- Keep all test code outside production sources. Use app/src/androidTest for Espresso; use testing/appium for external E2E.
- Page Object Model (POM): each screen should have a page object in testing/appium/pages with:
  - class ScreenNamePage(object):
      - locators as constants
      - actions as methods returning other page objects or values
- Locators:
  - Prefer resource-id (By.ID or accessibility_id). Example: "com.bersyte.noteapp:id/noteTitle"
  - Use content-desc/accessibility-id when available.
  - Avoid brittle XPaths; if necessary, centralize and document why.

Test naming & structure
- Tests: tests/test_<feature>_<flow>.py
- Page objects: pages/<screen>_page.py
- Fixtures: place shared data and setup/teardown in conftest.py and fixtures/
- Tagging: use pytest markers for smoke, regression, flaky. Example @pytest.mark.smoke

State & data management
- Tests must be idempotent and isolated. Reset app between tests by uninstalling/installing APK or using Appium capability noReset=false.
- Store reusable fixtures in testing/appium/fixtures and reference them in conftest.py.

Retries & Flaky tests
- Avoid coding retries inside tests; use pytest-rerunfailures in CI to reduce noise with a low retry limit (e.g., --reruns 1).
- Mark flaky tests with @pytest.mark.flaky and create tickets for owners.
- Capture screenshots and logs on failures and attach to CI job artifacts.

Logging, artifacts & debugging
- On failure, capture:
  - Screenshot (Appium driver.get_screenshot_as_file)
  - Device logs: adb logcat > logcat.txt
  - UI dumps if helpful
- Configure pytest to save these in a artifacts/ directory per test run.

CI recommendations (GitHub Actions example steps)
- PR workflow (fast):
  - Checkout
  - Set up JDK & Android SDK
  - ./gradlew test (unit tests)
  - ./gradlew assembleDebug
  - Start emulator and run small espresso smoke tests (connectedAndroidTest) only if emulator startup is acceptable
- Nightly workflow (full):
  - Build debug APK
  - Start emulator(s) or provision device farm
  - Start Appium server
  - Run pytest testing/appium/tests --maxfail=1 -q
  - Collect artifacts: screenshots, logs, pytest/allure results

Sample GitHub Action snippet (conceptual)
- name: Build APK
  run: ./gradlew assembleDebug
- name: Start emulator
  run: |-
    sdkmanager "system-images;android-33;google_apis;x86_64"
    avdmanager create avd -n test -k "system-images;android-33;google_apis;x86_64" --force
    emulator -avd test -no-window &
    ./wait-for-emulator.sh
- name: Run Appium tests
  run: |
    pip install -r testing/appium/requirements.txt
    appium &
    pytest testing/appium/tests -q

How to add a new test
1. Add a new Page Object under testing/appium/pages if new screen interactions are needed.
2. Add test under testing/appium/tests following naming conventions.
3. Add necessary fixtures to testing/appium/fixtures and update conftest.py.
4. Run locally and ensure tests pass on emulator(s).
5. Create PR with only test code changes and CI updates if needed. Reference test case IDs in PR description.

When you need a change in app behavior
- Do NOT change production code directly. Instead:
  - Discuss required hook with devs and request a test-only build variant or a test-only module under app/ with explicit approval, or
  - Use instrumentation-only approaches (app/src/androidTest) or external intercepting mocks in the test project.

Troubleshooting tips
- If locator fails: verify resource-id from APK using adb shell uiautomator dump and check hierarchy
- Emulator not booting: ensure correct x86_64 image installed and use -no-window for CI
- Appium connectivity: confirm device/emulator is visible via adb devices and port mapping for Appium

Contacts & ownership
- Test Manager: overall strategy and priorities
- Automation Engineers: test implementation and CI pipelines
- Developers: support for unit/integration tests and test-only modules

References
- testing/TEST_AUTOMATION_PLAN.md (project-level automation strategy)
- testing/appium/requirements.txt
- testing/appium/conftest.py
