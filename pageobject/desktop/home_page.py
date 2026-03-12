import allure
from playwright.sync_api import Page

from core.base_page import BasePage
from locator.desktop.home_page_locator import HomePageLocator


class HomePage(BasePage):
    """Amazon homepage page object."""

    @property
    def search_input(self): return self.page.locator(HomePageLocator.SEARCH_INPUT)

    @property
    def search_button(self): return self.page.locator(HomePageLocator.SEARCH_BUTTON)

    @property
    def account_link(self): return self.page.locator(HomePageLocator.ACCOUNT_LINK)

    @property
    def logo(self): return self.page.locator(HomePageLocator.LOGO)

    @property
    def nav_cart(self): return self.page.locator(HomePageLocator.NAV_CART)

    @property
    def flyout_signin(self): return self.page.locator(HomePageLocator.FLYOUT_SIGNIN).first

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
        self.hover(self.account_link, "Hello, Sign in")
        self.expect_visible(self.flyout_signin, "Sign in flyout button")
        self.click(self.flyout_signin, "Sign in flyout button")

    def get_account_label(self) -> str:
        return self.get_text(self.account_link)
