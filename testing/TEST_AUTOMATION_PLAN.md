Test Automation Strategy, Test Plan & Test Concept
For: mvvm_note_app_kotlin_android_studio
Author: Test Manager (7+ years in test management & automation)
Audience: Test Automation Engineers

Important rule
- Testers MUST NOT change application production code. All automation, helpers, test-only instrumentation and mocks must live in test folders or in a separate test project/module. Changes to the app codebase are not allowed.

1. Overview & Objectives
- Objective: Provide a stable, maintainable automation suite that verifies core app functionality (notes CRUD, search, navigation, data persistence) across local emulators and CI.
- Goals:
  - Fast unit-level feedback for logic (non-UI)
  - Reliable UI tests for critical flows (smoke/regression)
  - End-to-end tests via Appium for cross-device validation
  - CI integration to run test suites on pull requests and nightly builds

2. Scope
- In-scope features for automation:
  - App core flows: create/edit/delete notes, view note list, search notes
  - Navigation: open/close activities, back stack behavior
  - Persistence: local DB operations (Room) behavior from UI
  - Input validation and basic error handling
- Out-of-scope:
  - External integrations (none present in this app)
  - Performance and load testing

3. Test Pyramid & Strategy
- Unit tests (fast, many): business logic, utility functions. Run on JVM (Junit + Mockito/MockK). These are local unit tests only and should not modify production code.
- Integration tests (medium): repository/database interactions; prefer Robolectric or instrumentation tests when required. Keep these focused and deterministic.
- UI / E2E tests (slow, fewer): Appium-driven end-to-end tests that interact with the installed APK. Also maintain a small set of Espresso androidTest UI tests for in-repo instrumentation where allowed (tests only). Prefer Appium for cross-environment automation run from outside the app.

4. Frameworks & Tools
- Appium (UiAutomator2) for cross-device E2E tests. Desired capabilities already added in appium/DESIRED_CAPABILITIES.md.
- Espresso + AndroidX Test for instrumented UI tests (androidTest) — these run inside emulator via Gradle.
- JUnit5 or JUnit4 for unit tests. Use MockK for Kotlin mocking.
- Robolectric for JVM-based Android unit testing if needed.
- GitHub Actions for CI, executing emulator and/or Appium server.
- adb and emulator CLI for local testers.

5. Test Environment Matrix
- Local developer machines / emulators: Android 11 and Android 13 images recommended (api 30, 33). Ensure emulator architecture matches CI (x86_64 on CI typically).
- CI: Use GitHub Actions runners with Android emulator images (x86_64). Use Appium service or run instrumentation tests with Gradle.

6. Test Data & State Management
- Tests must be idempotent and independent. Each test should set up its own state.
- For UI/Appium tests: reset app state between tests (adb clear package or use capability noReset=false when launching via Appium), or use test-only endpoints to reset DB if added to test module.
- Store test data fixtures in a test/resources folder; avoid hard-coding values across tests.

7. Test Design & Canonical Test Cases (examples)
- Smoke (fast, run on PR):
  - Launch app, create a new note with title+body, verify it appears in list
  - Open existing note, edit body, save, verify changes
  - Delete a note and ensure it no longer appears
- Regression (E2E):
  - Create 3 notes, search for a substring, verify filtered results
  - Verify note persists after app restart (background/foreground)
  - Verify navigation: back button returns to list without duplicate entries
- Unit tests:
  - Validate ViewModel functions for saving and loading notes with mocked repository
  - Validate repository logic with in-memory DB (Robolectric or instrumentation if necessary)

8. Automation Architecture & Repo Structure (recommended)
- Create a top-level folder /testing or /e2e under repo root for external Appium tests.
- For in-repo tests:
  - app/src/test/java -> JVM unit tests
  - app/src/androidTest/java -> Espresso instrumentation tests (UI)
- External Appium test project structure (Node/Python/Java):
  - /testing/appium/
    - tests/
    - pages/ (Page Object Model for screens)
    - fixtures/
    - config/ (desired capabilities and environment configs)
    - ci/ (scripts to start emulator and appium on CI)
- Use Page Object Model (POM) for UI tests to isolate locators and actions.

9. Locators & Stability
- Prefer resource-id (android:id/...) for locating elements. Do not rely on visible text only.
- Where resource-ids are absent use content-desc or robust XPath as last resort.
- Keep locators in centralized page objects so updates are limited to tests.

10. Test Code Guidelines (tests-only changes)
- NEVER change production app code. If a test needs a hook (e.g., test-only network mock), add it under test-only modules or use instrumentation-only build variants. All changes must be in test sources or separate test project.
- Keep tests small and focused. One logical assertion per test where practical.
- Use setup/teardown to prepare/clean app state.
- Annotate flaky tests with a known tag and exclude from PR smoke runs until stabilized.

11. CI/CD Integration
- PR Gating (fast): run unit tests + smoke Espresso test suite (if emulator startup time acceptable). Use GitHub Actions matrix for Android API versions.
- Nightly (full): run Appium E2E test suite against emulator farm or hosted device provider.
- CI Steps (example):
  - Checkout
  - Set up JDK 11
  - Start Android SDK, create and start AVD (x86_64)
  - Build APK via ./gradlew assembleDebug
  - Start emulator and wait for boot
  - Start Appium server (if using external Appium tests)
  - Run Appium tests (python/Java/JS client) against emulator/device
  - Collect artifacts: logs, screenshots, video (if possible)

12. Flakiness and Resilience
- Add retries in CI for known-soft failures (but log each retry).
- Implement explicit waits and stable assertions, avoid brittle sleep-based waits.
- Capture screenshots and device logs on failures and attach to CI job artifacts.

13. Reporting & Metrics
- Test execution dashboard (e.g., Allure) for daily health metrics
- Track: pass rate, flakiness rate, mean time to repair (MTTR) per test, and average runtime
- Maintain a list of flaky tests with owners and action plan

14. Security, Permissions, and Privacy
- Do not include real user data in tests. Use synthetic fixtures only.
- Keep any API keys or secrets out of test repo; use CI secrets if needed.

15. Onboarding & Responsibilities
- Test Automation Engineer responsibilities:
  - Implement tests according to this plan
  - Keep tests isolated and only edit test code
  - Maintain page objects and locators
  - Fix test flakiness and own flaky test backlog
- Test Manager responsibilities:
  - Prioritize test coverage based on risk
  - Review CI test health and adjust scope

16. Deliverables & Timeline (suggested)
- Week 1: Setup test project skeleton (/testing), CI job skeleton, basic smoke tests (create/edit/delete)
- Week 2: Expand unit tests and add integration tests for repository
- Week 3: Add Appium E2E tests for core flows; stabilize on CI
- Ongoing: add tests for additional flows and track flakiness

17. Example quick-start commands (for test engineers)
- Build app (locally):
  export JAVA_HOME=$(/usr/libexec/java_home -v 11)
  ./gradlew assembleDebug
- Start emulator:
  emulator -avd <AVD_NAME>
- Install APK (if built locally):
  adb install -r app/build/outputs/apk/debug/app-debug.apk
- Run Appium tests (example if python client used):
  cd testing/appium
  pip install -r requirements.txt
  pytest -q

18. Next steps I will perform on request
- Create a testing skeleton (Appium test project with POM and sample smoke tests) in /testing/appium that only changes tests and test config.
- Create GitHub Actions workflow to run smoke tests on PRs (using emulator x86_64).

Contact
- If you approve, I will create the testing skeleton next. Please confirm “Create testing skeleton” or ask for adjustments to the plan.
