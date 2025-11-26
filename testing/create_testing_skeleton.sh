#!/usr/bin/env bash
set -e
ROOT="$(pwd)"
mkdir -p testing/appium/tests testing/appium/pages testing/appium/config .github/workflows

cat > testing/appium/requirements.txt <<'PYREQ'
appium-python-client==3.6.0
pytest==7.4.0
pytest-xdist==3.3.1
PYREQ

cat > testing/appium/config/capabilities.json <<'CAP'
{
  "platformName": "Android",
  "platformVersion": "11",
  "deviceName": "emulator-5554",
  "automationName": "UiAutomator2",
  "appPackage": "com.bersyte.noteapp",
  "appActivity": ".MainActivity",
  "noReset": false
}
CAP

cat > testing/appium/conftest.py <<'PY'
import json
import os
import pytest
from appium import webdriver

ROOT = os.path.dirname(__file__)
CAP_PATH = os.path.join(ROOT, 'config', 'capabilities.json')

@pytest.fixture(scope='session')
def capabilities():
    with open(CAP_PATH) as f:
        return json.load(f)

@pytest.fixture(scope='session')
def driver(capabilities):
    url = os.environ.get('APPIUM_SERVER', 'http://localhost:4723/wd/hub')
    driver = webdriver.Remote(url, capabilities)
    yield driver
    try:
        driver.quit()
    except Exception:
        pass
PY

cat > testing/appium/pages/home_page.py <<'PY'
from appium.webdriver.common.appiumby import AppiumBy

class HomePage:
    # resource ids from app
    ADD_BUTTON = (AppiumBy.ID, 'com.bersyte.noteapp:id/fab')
    NOTE_TITLE_INPUT = (AppiumBy.ID, 'com.bersyte.noteapp:id/etTitle')
    NOTE_BODY_INPUT = (AppiumBy.ID, 'com.bersyte.noteapp:id/etBody')
    SAVE_BUTTON = (AppiumBy.ID, 'com.bersyte.noteapp:id/btnSave')
    NOTES_RECYCLER = (AppiumBy.ID, 'com.bersyte.noteapp:id/recyclerView')

    def __init__(self, driver):
        self.driver = driver

    def tap_add(self):
        self.driver.find_element(*self.ADD_BUTTON).click()

    def enter_title(self, title):
        self.driver.find_element(*self.NOTE_TITLE_INPUT).send_keys(title)

    def enter_body(self, body):
        self.driver.find_element(*self.NOTE_BODY_INPUT).send_keys(body)

    def tap_save(self):
        self.driver.find_element(*self.SAVE_BUTTON).click()

    def has_note_with_title(self, title):
        elems = self.driver.find_elements(*self.NOTES_RECYCLER)
        # simple check: any element text contains title
        for e in elems:
            if title in e.text:
                return True
        return False
PY

cat > testing/appium/tests/test_smoke_create_note.py <<'PY'
import time
from testing.appium.pages.home_page import HomePage


def test_create_note_smoke(driver):
    home = HomePage(driver)
    # ensure we're on home screen then create a note
    home.tap_add()
    title = f"E2E Note {int(time.time())}"
    home.enter_title(title)
    home.enter_body('This is a test note')
    home.tap_save()
    # small wait for UI transition
    time.sleep(1)
    assert home.has_note_with_title(title)
PY

cat > .github/workflows/appium-tests.yml <<'YML'
name: Appium E2E Tests
on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  e2e:
    runs-on: macos-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up JDK 11
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '11'

      - name: Install Android SDK tools
        uses: android-actions/setup-android@v2
        with:
          api-level: 30
          target: default
          ndk: false

      - name: Build APK
        run: |
          export JAVA_HOME=$(/usr/libexec/java_home -v 11)
          ./gradlew assembleDebug -p ./

      - name: Start emulator
        run: |
          echo "Starting emulator..."
          nohup $ANDROID_SDK_ROOT/emulator/emulator -avd test -no-window -no-audio &

      - name: Wait for emulator
        run: adb wait-for-device

      - name: Install APK
        run: adb install -r app/build/outputs/apk/debug/app-debug.apk || true

      - name: Start Appium server
        run: |
          npm install -g appium
          nohup appium &

      - name: Run Appium tests
        run: |
          python3 -m pip install -r testing/appium/requirements.txt
          pytest -q testing/appium/tests
YML

chmod +x testing/create_testing_skeleton.sh

echo "Testing skeleton creation script written to testing/create_testing_skeleton.sh"
