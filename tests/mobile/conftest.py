import os

import allure
import pytest
import yaml
from playwright.sync_api import Playwright

from core.config import config


# --- Load device profiles from devices/devices.yaml ---

def _load_devices() -> dict:
    path = os.path.join(os.path.dirname(__file__), "..", "..", "devices", "devices.yaml")
    with open(path) as f:
        return yaml.safe_load(f)


# --- Playwright mobile fixture ---

@pytest.fixture
def mobile_page(playwright: Playwright, mobile_device_name: str):
    """Playwright page with mobile device emulation.

    Loads device profile from devices/devices.yaml.
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


# --- Screenshot on failure for mobile_page ---

@pytest.fixture(autouse=True)
def mobile_screenshot_on_failure(request):
    """Capture screenshot and attach to Allure report on mobile test failure."""
    yield
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        mobile_page = request.node.funcargs.get("mobile_page")
        if mobile_page:
            allure.attach(
                mobile_page.screenshot(),
                name=f"FAILED - {request.node.name}",
                attachment_type=allure.attachment_type.PNG,
            )
