import allure
import pytest
from playwright.sync_api import Page

from core.config import config


# --- Browser configuration fixtures ---

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override default Playwright browser context with values from config."""
    bc = config.browser_config
    return {
        **browser_context_args,
        "viewport": {"width": bc.viewport_width, "height": bc.viewport_height},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Override default Playwright browser launch args with values from config."""
    bc = config.browser_config
    return {
        **browser_type_launch_args,
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
