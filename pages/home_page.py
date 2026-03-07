import allure
from playwright.sync_api import Page

from core.base_page import BasePage


class HomePage(BasePage):
    """Amazon homepage page object."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = page.locator("#twotabsearchtextbox")
        self.search_button = page.locator("#nav-search-submit-button")
        self.account_link = page.locator("#nav-link-accountList")
        self.logo = page.locator("#nav-logo-sprites, #nav-bb-logo")
        self.nav_cart = page.locator("#nav-cart")

    @allure.step("Open Amazon homepage")
    def open(self) -> "HomePage":
        self.navigate("/")
        return self

    @allure.step("Verify Amazon homepage is loaded")
    def verify_loaded(self) -> "HomePage":
        self.expect_visible(self.search_input, "Search bar")
        self.expect_visible(self.nav_cart, "Cart icon")
        return self

    @allure.step("Search for '{term}'")
    def search(self, term: str) -> None:
        self.fill(self.search_input, term, "Search box")
        self.click(self.search_button, "Search button")

    @allure.step("Go to sign in via account flyout")
    def go_to_signin(self) -> None:
        flyout_signin = self.page.locator("#nav-flyout-ya-signin a").first
        self.hover(self.account_link, "Hello, Sign in")
        self.expect_visible(flyout_signin, "Sign in flyout button")
        self.click(flyout_signin, "Sign in flyout button")

    def get_account_label(self) -> str:
        return self.get_text(self.account_link)
