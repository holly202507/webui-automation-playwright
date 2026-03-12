import allure
from playwright.sync_api import Page

from core.base_page import BasePage
from locator.mobile.home_page_locator import MobileHomePageLocator


class MobileHomePage(BasePage):
    """Amazon homepage page object for mobile web.

    Key differences from desktop:
    - No hover flyout for sign-in; the account link navigates directly.
    - Hamburger menu (#nav-hamburger-menu) replaces the top nav links.
    """

    @property
    def search_input(self): return self.page.locator(MobileHomePageLocator.SEARCH_INPUT)

    @property
    def search_button(self): return self.page.locator(MobileHomePageLocator.SEARCH_BUTTON)

    @property
    def account_link(self): return self.page.locator(MobileHomePageLocator.ACCOUNT_LINK)

    @property
    def logo(self): return self.page.locator(MobileHomePageLocator.LOGO)

    @property
    def nav_cart(self): return self.page.locator(MobileHomePageLocator.NAV_CART)

    @property
    def hamburger_menu(self): return self.page.locator(MobileHomePageLocator.HAMBURGER_MENU)

    @allure.step("Open Amazon homepage")
    def open(self) -> "MobileHomePage":
        self.navigate("/")
        return self

    @allure.step("Verify Amazon homepage is loaded")
    def verify_loaded(self) -> "MobileHomePage":
        self.expect_visible(self.search_input, "Search bar")
        self.expect_visible(self.nav_cart, "Cart icon")
        return self

    @allure.step("Search for '{term}'")
    def search(self, term: str) -> None:
        self.fill(self.search_input, term, "Search box")
        self.click(self.search_button, "Search button")

    @allure.step("Go to sign in on mobile")
    def go_to_signin(self) -> None:
        # Mobile: no hover flyout — clicking the account link navigates directly
        self.click(self.account_link, "Account / Sign in link")

    def get_account_label(self) -> str:
        return self.get_text(self.account_link)
