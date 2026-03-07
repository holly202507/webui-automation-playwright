import allure
from playwright.sync_api import Locator, Page, expect

from core.config import config


class BasePage:
    """Base class for all page objects. Wraps Playwright actions with
    Allure step logging, automatic screenshots per step, and centralised
    timeout management."""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = config.timeout

    # --- Internal screenshot helper ---

    def _screenshot(self, name: str) -> None:
        """Capture the current page and attach it to the active Allure step."""
        allure.attach(
            self.page.screenshot(full_page=False),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )

    # --- Navigation ---

    def navigate(self, path: str = "") -> None:
        url = f"{config.base_url.rstrip('/')}{path}"
        with allure.step(f"Navigate to {url}"):
            self.page.goto(url)
            self._screenshot(f"Navigate to {url}")

    # --- Actions ---

    def click(self, locator: Locator, description: str = "") -> None:
        label = description or locator.__str__()
        with allure.step(f"Click '{label}'"):
            locator.click()
            self._screenshot(f"After click '{label}'")

    def hover(self, locator: Locator, description: str = "") -> None:
        label = description or locator.__str__()
        with allure.step(f"Hover over '{label}'"):
            locator.hover()
            self._screenshot(f"After hover '{label}'")

    def fill(self, locator: Locator, value: str, description: str = "") -> None:
        label = description or locator.__str__()
        with allure.step(f"Fill '{label}' with '{value}'"):
            locator.fill(value)
            self._screenshot(f"After fill '{label}'")

    def select_option(self, locator: Locator, value: str, description: str = "") -> None:
        label = description or locator.__str__()
        with allure.step(f"Select '{value}' in '{label}'"):
            locator.select_option(value)
            self._screenshot(f"After select '{value}' in '{label}'")

    def get_text(self, locator: Locator) -> str:
        return locator.inner_text()

    def is_visible(self, locator: Locator) -> bool:
        return locator.is_visible()

    # --- Waits & Assertions ---

    def expect_visible(self, locator: Locator, description: str = "") -> None:
        label = description or locator.__str__()
        with allure.step(f"Expect '{label}' to be visible"):
            expect(locator).to_be_visible(timeout=self.timeout)
            self._screenshot(f"Visible: '{label}'")

    def expect_hidden(self, locator: Locator, description: str = "") -> None:
        label = description or locator.__str__()
        with allure.step(f"Expect '{label}' to be hidden"):
            expect(locator).to_be_hidden(timeout=self.timeout)
            self._screenshot(f"Hidden: '{label}'")

    def expect_text(self, locator: Locator, text: str) -> None:
        with allure.step(f"Expect element text to equal '{text}'"):
            expect(locator).to_have_text(text, timeout=self.timeout)
            self._screenshot(f"Text equals '{text}'")

    def expect_url_contains(self, fragment: str) -> None:
        with allure.step(f"Expect URL to contain '{fragment}'"):
            expect(self.page).to_have_url(f"**{fragment}**", timeout=self.timeout)
            self._screenshot(f"URL contains '{fragment}'")

    def wait_for_url(self, url_pattern: str) -> None:
        with allure.step(f"Wait for URL '{url_pattern}'"):
            self.page.wait_for_url(url_pattern, timeout=self.timeout)
            self._screenshot(f"URL matched '{url_pattern}'")

    # --- Utilities ---

    def take_screenshot(self, name: str = "screenshot") -> None:
        """Manually attach a screenshot to the current Allure step."""
        self._screenshot(name)

    @property
    def title(self) -> str:
        return self.page.title()
