import json
import os
import pytest
import time
from appium import webdriver

ROOT = os.path.dirname(__file__)
CAP_PATH = os.path.join(ROOT, 'config', 'capabilities.json')
ARTIFACTS_DIR = os.path.join(ROOT, 'artifacts')


@pytest.fixture(scope='session')
def capabilities():
    with open(CAP_PATH) as f:
        return json.load(f)


@pytest.fixture(scope='session')
def driver(capabilities):
    """Create a single Appium session for the test session.

    Note: Tests should remain idempotent and reset app state between tests when needed.
    This fixture will quit the driver at the end of the session.
    """
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    url = os.environ.get('APPIUM_SERVER')

    # If APPIUM_SERVER is not provided, skip E2E tests to allow local lint/collection runs.
    if not url:
        pytest.skip("APPIUM_SERVER not set - skipping Appium E2E tests", allow_module_level=True)

    # Use an Options object when available (compatible with recent selenium/appium clients).
    try:
        from appium.options.android import AndroidOptions

        opts = AndroidOptions()
        for k, v in capabilities.items():
            opts.set_capability(k, v)
        driver = webdriver.Remote(command_executor=url, options=opts)
    except Exception:
        # Fallback to older constructor signature if options API isn't available
        try:
            driver = webdriver.Remote(command_executor=url, desired_capabilities=capabilities)
        except Exception:
            # as a last resort, try calling with minimal args and let the error surface
            driver = webdriver.Remote(command_executor=url)

    yield driver
    try:
        driver.quit()
    except Exception:
        pass




def _safe_filename(s: str) -> str:
    return s.replace('/', '_').replace('::', '_').replace(' ', '_')


def pytest_runtest_makereport(item, call):
    """Hook to capture artifacts (screenshot, page source, device logs) on test failures.

    Creates artifacts/<test_nodeid>/ with files:
      - screenshot.png
      - page_source.xml
      - logcat.txt (if available)

    This hook uses the driver fixture when available.
    """
    # only act on the call phase (not setup/teardown)
    if call.when != 'call':
        return

    report = pytest.TestReport.from_item_and_call(item, call)
    if report.failed:
        driver = item.funcargs.get('driver', None)
        nodeid = _safe_filename(item.nodeid)
        dest_dir = os.path.join(ARTIFACTS_DIR, nodeid)
        os.makedirs(dest_dir, exist_ok=True)

        if driver:
            # screenshot
            try:
                screenshot_path = os.path.join(dest_dir, 'screenshot.png')
                driver.get_screenshot_as_file(screenshot_path)
            except Exception:
                # ignore screenshot failures
                pass

            # page source
            try:
                page_src = driver.page_source
                with open(os.path.join(dest_dir, 'page_source.xml'), 'w', encoding='utf-8') as f:
                    f.write(page_src)
            except Exception:
                pass

            # device logs (logcat) - may not be available on all setups
            try:
                logs = driver.get_log('logcat')
                with open(os.path.join(dest_dir, 'logcat.txt'), 'w', encoding='utf-8') as f:
                    for entry in logs:
                        f.write(f"{entry.get('timestamp')} {entry.get('level')} {entry.get('message')}\n")
            except Exception:
                # fallback: try to run adb logcat if ANDROID_SERIAL provided
                try:
                    android_serial = os.environ.get('ANDROID_SERIAL')
                    if android_serial:
                        import subprocess
                        out_path = os.path.join(dest_dir, 'logcat.txt')
                        with open(out_path, 'wb') as outf:
                            subprocess.run(['adb', '-s', android_serial, 'logcat', '-d'], stdout=outf, stderr=subprocess.DEVNULL)
                except Exception:
                    pass

        # If no driver is available, still record a marker file
        else:
            with open(os.path.join(dest_dir, 'note.txt'), 'w') as f:
                f.write('No driver fixture available to capture artifacts.')

    return report
