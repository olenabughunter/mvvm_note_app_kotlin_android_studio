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

What the automation engineer implemented (current state)
- A small Appium E2E suite in testing/appium/tests covering create, edit, delete flows.
- Page Objects implemented in testing/appium/pages (HomePage, NewNotePage, UpdateNotePage) following POM patterns.
- A Waits helper (testing/appium/waits.py) wrapping WebDriverWait and common wait operations.
- conftest.py provides a session-scoped driver fixture and robust test failure artifact capture (screenshot, page source, logcat fallback).
- GitHub Actions workflow (.github/workflows/appium-tests.yml) that boots an emulator, builds the debug APK, installs dependencies, starts Appium and runs pytest; artifacts are uploaded from testing/appium/artifacts.

Quick-start (local)

VSCode users: If you see "Import \"pytest\" could not be resolved" in the editor, add workspace settings to quiet missing-import diagnostics or configure your Python interpreter/extraPaths. Example file to add to the repo:

.vscode/settings.json
```
{
  "python.analysis.diagnosticSeverityOverrides": {
    "reportMissingImports": "none"
  },
  "python.analysis.typeCheckingMode": "off"
}
```

Alternatively set python.analysis.extraPaths to your virtualenv site-packages or select the project interpreter in VSCode. These changes only affect the editor diagnostics and do not change test execution.

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
  appium --port 4723 &
  export APPIUM_SERVER=http://127.0.0.1:4723/wd/hub
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
  - Prefer resource-id (By.ID or accessibility_id). Example: "com.bersyte.noteapp:id/tvNoteTitle"
  - Use content-desc/accessibility-id when available.
  - Avoid brittle XPaths; if necessary, centralize and document why.

Test naming & structure
- Tests: tests/test_<feature>_<flow>.py
- Page objects: pages/<screen>_page.py
- Fixtures: place shared data and setup/teardown in conftest.py and fixtures/
- Tagging: use pytest markers for smoke, regression, flaky. Example @pytest.mark.smoke

State & data management
- Tests must be idempotent and isolated. Reset app between tests by uninstalling/installing APK or using Appium capability noReset=false, or explicitly call driver.reset() in setup fixtures.
- Store reusable fixtures in testing/appium/fixtures and reference them in conftest.py.

Retries & Flaky tests
- Avoid coding retries inside test logic; use pytest-rerunfailures in CI to reduce noise with a low retry limit (e.g., --reruns 1).
- Mark flaky tests with @pytest.mark.flaky and create tickets for owners.
- Capture screenshots and logs on failures and attach to CI job artifacts.

Logging, artifacts & debugging
- On failure, capture:
  - Screenshot (Appium driver.get_screenshot_as_file)
  - Device logs: driver.get_log('logcat') or adb logcat via ANDROID_SERIAL fallback
  - Page source (driver.page_source)
- Configure pytest to save these in testing/appium/artifacts/<test_nodeid>/ for CI collection.

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
  - Install APK onto emulator: adb -s $ANDROID_EMULATOR install -r app/build/outputs/apk/debug/app-debug.apk
  - Start Appium server
  - Run pytest testing/appium/tests --reruns 1 -q
  - Collect artifacts: screenshots, logs, pytest/allure results

Suggested improvements and rationale (added after reviewing the implemented suite)
1) Driver scope & test isolation
- Current conftest: driver fixture is session-scoped which means a single Appium session is reused for all tests. That improves speed but risks state leakage between tests and makes test parallelization harder.
- Recommendation: Prefer a function-scoped driver fixture or add a per-test reset fixture that calls driver.reset() or reinstalls the app between tests. If speed is a concern, keep session scope but ensure each test explicitly resets app state (e.g., driver.reset()). Document chosen approach in conftest and Automation Instructions.

2) App install & readiness in CI
- Ensure the built APK is installed on the emulator before running tests. The current workflow builds the APK but does not install it explicitly; Appium may install automatically but explicit install improves determinism.
- Add a step in the workflow: adb -s $ANDROID_EMULATOR install -r app/build/outputs/apk/debug/app-debug.apk

3) APPIUM_SERVER and environment variables
- conftest skips tests when APPIUM_SERVER is not set. In CI ensure APPIUM_SERVER is exported (example: export APPIUM_SERVER=http://127.0.0.1:4723/wd/hub) so tests do not silently skip. Document this in CI steps and README.

4) CI failure handling & retries
- In the current workflow tests run with continue-on-error: true which hides failures. Change to let the job fail and use pytest-rerunfailures to rerun flaky tests. Example:
  - run: pytest testing/appium/tests --reruns 1 -q
  (remove continue-on-error)

5) Faster emulator boot & stability
- Use an emulator snapshot or reuse AVD between runs in CI to reduce boot time if supported by runner. Add a reliable wait-for-boot helper (check sys.boot_completed and adb shell wm size) and ensure emulator is responsive before installing APK or starting Appium.

6) Collect more diagnostics on failure
- The conftest already captures many artifacts. Additionally capture:
  - adb bugreport (if storage allows) or trimmed logs
  - device screenshots at key steps (optional) for richer debugging

7) Test timeouts & explicit waits
- Tests use Waits helper but some fallbacks use driver.back() or open_notifications(); be explicit in documentation about expected app behaviors so page objects are robust. Consider replacing ambiguous fallbacks with clear checks and documented assumptions.

8) Test markers and CI selection
- Use pytest markers to run smoke vs full suites in CI (PR -> smoke, nightly -> regression). The repo already marks tests but make sure CI passes marker args when running specific suites (pytest -m smoke).

9) Dependency pinning & reproducibility
- Pin key deps in testing/appium/requirements.txt (appium-python-client, pytest, pytest-rerunfailures). CI should install pinned versions for reproducible runs.

10) Accessibility & locators
- Verify resource-id stability across releases. If resource-ids change often, add a locator mapping file and document how to update page objects.

How to add these improvements (practical snippets)
- Example: CI step to install APK and set APPIUM_SERVER (add before running pytest):
  - name: Install APK
    run: adb -s $ANDROID_EMULATOR install -r app/build/outputs/apk/debug/app-debug.apk
  - name: Start Appium server
    run: |
      appium --port 4723 > appium.log 2>&1 &
      sleep 3
      export APPIUM_SERVER=http://127.0.0.1:4723/wd/hub

- Example: Run pytest with reruns (remove continue-on-error):
  run: |
    pip install -r testing/appium/requirements.txt
    pytest testing/appium/tests --reruns 1 -q

- Example: Per-test reset fixture (alternative to changing driver scope):
  @pytest.fixture(autouse=True)
  def reset_app_between_tests(driver):
      # ensure clean state
      try:
          driver.reset()
      except Exception:
          pass
      yield
      # optional post-test cleanup

Practical next steps for automation engineers
- Decide driver scope: keep session scope + autouse reset fixture OR change to function scope driver fixture. Implement in conftest.py with tests that verify isolation.
- Update CI workflow to explicitly install APK, export APPIUM_SERVER, remove continue-on-error and run pytest with reruns.
- Pin dependency versions in requirements.txt and add a requirements.lock if needed.
- Add a small README_AUTOMATION.md quick-start (there is one under testing/appium/README_AUTOMATION.md) — keep it in sync with these instructions.

How to propose changes to production app behavior
- DO NOT change app/src/main directly. Request test-only modules or build variants from devs and ensure changes are added to test sources only.

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
