import os

import allure
import pytest
import yaml
from playwright.sync_api import Playwright

from core.config import config


# --- Load device profiles from mobile/devices.yaml ---

def _load_devices() -> dict:
    path = os.path.join(os.path.dirname(__file__), "..", "..", "mobile", "devices.yaml")
    with open(path) as f:
        return yaml.safe_load(f)


def _load_browserstack_config() -> dict:
    path = os.path.join(os.path.dirname(__file__), "..", "..", "mobile", "browserstack.yml")
    with open(path) as f:
        return yaml.safe_load(f)


# --- Playwright mobile fixture (PR runs) ---

@pytest.fixture
def mobile_page(playwright: Playwright, mobile_device_name: str):
    """Playwright page with mobile device emulation.

    Used for PR runs on BrowserStack or locally.
    Loads device profile from mobile/devices.yaml.
    Override device with: pytest --mobile-device samsung_galaxy_s23
    """
    devices = _load_devices()
    device_profile = devices["playwright"][mobile_device_name]

    # playwright.devices contains real-world device presets
    # (viewport, user agent, touch support, pixel ratio, etc.)
    pw_device = playwright.devices[device_profile["device_name"]]

    # Launch the right browser engine: webkit (iOS Safari) or chromium (Android Chrome)
    browser_type = getattr(playwright, device_profile["browser"])
    browser = browser_type.launch(
        headless=config.browser_config.headless,
        slow_mo=config.browser_config.slow_mo,
    )
    context = browser.new_context(**pw_device)
    page = context.new_page()

    yield page

    context.close()
    browser.close()


# --- Appium fixture (nightly real iOS Safari) ---

@pytest.fixture(scope="session")
def appium_driver(mobile_device_name: str):
    """Appium WebDriver for nightly real iOS Safari testing on BrowserStack.

    Requires environment variables:
        BROWSERSTACK_USERNAME
        BROWSERSTACK_ACCESS_KEY

    Run nightly with:
        pytest tests/mobile/ -m safari --mobile-device iphone_14
    """
    from appium import webdriver as appium_webdriver
    from appium.options import XCUITestOptions

    devices = _load_devices()
    bs_config = _load_browserstack_config()
    caps = devices["appium"][mobile_device_name]

    options = XCUITestOptions()
    options.platform_version = caps["platform_version"]
    options.device_name = caps["device_name"]
    options.browser_name = caps["browser"]

    options.load_capabilities({
        "bstack:options": {
            "projectName": bs_config["project"],
            "buildName": bs_config["build"],
            "sessionName": bs_config["session"],
            "userName": os.getenv("BROWSERSTACK_USERNAME"),
            "accessKey": os.getenv("BROWSERSTACK_ACCESS_KEY"),
        }
    })

    driver = appium_webdriver.Remote(
        command_executor="https://hub-cloud.browserstack.com/wd/hub",
        options=options,
    )

    yield driver

    driver.quit()


# --- Screenshot on failure for mobile_page ---

@pytest.fixture(autouse=True)
def mobile_screenshot_on_failure(request):
    """Capture screenshot and attach to Allure report on mobile test failure."""
    yield
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        # mobile_page fixture may not be present in every test (e.g. appium tests)
        mobile_page = request.node.funcargs.get("mobile_page")
        if mobile_page:
            allure.attach(
                mobile_page.screenshot(),
                name=f"FAILED - {request.node.name}",
                attachment_type=allure.attachment_type.PNG,
            )
