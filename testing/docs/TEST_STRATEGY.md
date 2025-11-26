Test Strategy
For: mvvm_note_app_kotlin_android_studio
Author: Test Manager (7+ years - mobile & web testing, automation)
Audience: Testers, Test Automation Engineers, Devs, Stakeholders

1. Overview
This Test Strategy translates the Test Concept into a practical approach for designing and executing tests on the MVVM Note App. It defines how we select tests, environments, tools, and responsibilities.

2. Objectives
- Focus automation effort on high-risk, high-value flows (notes CRUD, persistence, navigation).
- Provide fast feedback loops on PRs via unit tests and limited instrumentation smoke tests.
- Maintain a small, reliable E2E suite for nightly/CI validation across emulator/device matrix.

3. Test Levels & Responsibilities
- Unit Tests (Owner: Devs/Testers): cover ViewModel logic, utilities. Run locally and on CI. Use MockK for Kotlin mocks.
- Integration Tests (Owner: Testers/Devs): repository and DB interactions using Robolectric or instrumentation tests.
- Instrumentation UI Tests (Owner: Testers): Espresso tests located under app/src/androidTest for small smoke flows only.
- E2E Tests (Owner: Test Automation Engineers): External Appium project under /testing/appium for cross-device verification.

4. Test Selection Criteria
- Include in PR-triggered runs: all unit tests + small espresso smoke suite (create/edit/delete) if emulator startup is acceptable.
- Include in nightly: full Appium E2E suite + expanded espresso tests + integration tests.
- Prioritize tests that validate data integrity, navigation, and critical user journeys.

5. Test Design Principles
- Single responsibility: tests should verify one logical behavior per test.
- Deterministic setup: each test sets its own state with fixtures or by resetting app data.
- Use POM for UI tests to centralize locators and actions.
- Prefer resource-id selectors; avoid brittle XPaths.

6. Environments & Matrix
- Local: Emulators for API 30 and 33 (x86_64). Real devices optional for exploratory runs.
- CI: GitHub Actions using x86_64 emulators. Appium server run as a step or use hosted device/cloud provider.
- App variants: use debug APK for tests. Tests must not rely on developer settings or debug-only flags inside production code.

7. Tooling & Frameworks
- Unit: JUnit + MockK
- Integration: Robolectric or instrumentation tests
- Instrumentation UI: Espresso + AndroidX Test
- E2E: Appium with Python/Java/JS client (Python client already present under testing/appium)
- Reporting: pytest + allure for python-based Appium tests; Gradle test report for Android tests

8. Test Data Management
- Keep fixtures in testing/appium/fixtures and app/src/test/resources for JVM tests.
- Use randomized but controlled values to avoid collisions.
- Reset app data between tests via adb uninstall/install or Appium capability noReset=false.

9. CI Configuration
- PR workflow: run unit tests, build debug APK, run espresso smoke tests (optional) in parallel.
- Nightly workflow: build APK, start emulator, run Appium tests against emulator or device farm.
- Persist artifacts: logs, screenshots, video (when available).

10. Flakiness Handling
- Each flaky test must be annotated in test metadata with a ticket/owner.
- Implement retries only in CI layer with clear logging of retry attempts.
- Review flaky tests weekly and either fix or quarantine.

11. Test Metrics & Reporting
- Track pass/fail rates, execution time, flaky tests count, and trend per test suite.
- Use Allure or similar to provide readable reports with attachments (screenshots/logs)

12. Security & Compliance
- Do not store secrets inside test repo; use CI secrets for service credentials if needed.
- Use synthetic test data only.

13. Onboarding & Documentation
- Provide quick-start README in /testing/appium with setup steps (requirements, AVD setup, run commands).
- Include the Test Concept, Strategy, and Plan in testing/docs for quick reference.

14. Escalation & Ownership
- Test Manager: test coverage priorities, flakiness reviews, CI health
- Automation Engineers: implement and maintain E2E tests and CI pipelines
- Developers: support with unit/integration tests and provide test hooks if added in test-only modules

15. Constraints Reminder
- No modifications to production app source code by testers. Test-only changes must live in test folders or external test project.

16. Next Steps
- Create automation project skeleton and minimal smoke tests in /testing/appium (on request)
