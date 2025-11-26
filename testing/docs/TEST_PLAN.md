Test Plan
For: mvvm_note_app_kotlin_android_studio
Author: Test Manager (7+ years - mobile & web testing, automation)
Audience: Testers, Test Automation Engineers, Project Managers

1. Scope & Objectives
Scope aligns with Test Concept: core flows (create/edit/delete/search notes), navigation, and persistence. Objective: ensure each release meets functional quality gates and maintain test automation to reduce regression risk.

2. Test Items
- App APK (debug) produced via ./gradlew assembleDebug
- Unit test suites (app/src/test)
- Instrumentation UI tests (app/src/androidTest)
- Appium E2E tests (testing/appium)

3. Features to be Tested
- Create note: title + body required? (app currently allows empty body) - tests will assert expected behavior
- Edit note: changes persist
- Delete note: removed from list
- Search: filter by substring
- Navigation: back stack, fragment transitions
- Persistence: notes remain after app restart

4. Features not to be Tested
- Performance/load
- Device-specific UI rendering variations beyond emulator/device combinations in test matrix

5. Approach
- Unit tests: write and maintain in app/src/test. Run on every PR.
- Instrumentation tests: small smoke tests to run on PRs if emulator startup cost acceptable. Run full suite nightly.
- Appium E2E: external end-to-end tests for cross-device coverage. Run on nightly and release pipelines.
- Manual exploratory testing: ad-hoc sessions by QA to cover UX and edge cases.

6. Test Deliverables
- Test reports (CI artifacts)
- Automated test suites under testing/ and app/src/test, app/src/androidTest
- Test data fixtures and POMs under testing/appium
- This Test Plan and Strategy docs

7. Entry and Exit Criteria
- Entry: feature branch with passing unit tests and buildable APK
- Exit: all smoke tests pass; no critical/blocker defects open; regression suite run completed for release

8. Resources & Roles
- Test Manager: prioritize tests, review results
- Automation Engineers: implement Appium tests and CI pipelines
- Developers: provide fixes and unit/integration tests support
- CI: GitHub Actions runners with Android SDK and emulator support

9. Schedule
- Week 1: setup skeleton, unit tests, PR smoke tests
- Week 2: expand integration tests and more instrumentation tests
- Week 3: implement Appium flows and CI nightly runs

10. Test Environment
- Local: dev machines with Android SDK and AVDs
- CI: GitHub Actions, Android emulators, Appium server

11. Risks & Contingencies
- Emulator instability: use retries and ensure correct AVD images
- Flaky tests: quarantine and fix ownership

12. Dependencies
- Android SDK and emulator images availability on CI
- Appium server and correct device capabilities

13. Test Case Examples (IDs will be created in the test management tool)
- TC_SMOKE_001: Launch app and create a note -> verify list
- TC_SMOKE_002: Edit a note and verify changes
- TC_SMOKE_003: Delete a note and verify it is removed
- TC_REG_001: Create multiple notes, search by substring, verify results

14. Execution & Reporting
- PRs: run unit tests and smoke instrumentation tests; failures block merge
- Nightly: run full E2E and instrumentation suites; report via Allure dashboards

15. Approval
- QA Lead and Product Owner sign-off required before release
