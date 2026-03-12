import allure
import pytest
from playwright.sync_api import Page

from core.config import config


# --- CLI options ---

def pytest_addoption(parser):
    parser.addoption(
        "--mobile-device",
        default="iphone_14",
        help="Mobile device profile to use for mobile tests (defined in mobile/devices.yaml). "
             "Example: --mobile-device samsung_galaxy_s23",
    )


@pytest.fixture(scope="session")
def mobile_device_name(request) -> str:
    """Session-scoped fixture that exposes the --mobile-device CLI option."""
    return request.config.getoption("--mobile-device")


# --- Desktop browser configuration fixtures ---

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override default Playwright browser context with values from config."""
    bc = config.browser_config
    return {
        **browser_context_args,  # keep existing defaults
        "viewport": {"width": bc.viewport_width, "height": bc.viewport_height},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Override default Playwright browser launch args with values from config."""
    bc = config.browser_config
    return {
        **browser_type_launch_args,  # keep existing defaults
        "headless": bc.headless,
        "slow_mo": bc.slow_mo,
    }


# --- Screenshot on failure ---

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test phase results on the item so fixtures can inspect them."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page, request):
    """Automatically capture and attach a screenshot to Allure on test failure."""
    yield
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=f"FAILED - {request.node.name}",
            attachment_type=allure.attachment_type.PNG,
        )
