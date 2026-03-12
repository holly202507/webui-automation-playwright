import allure
from playwright.sync_api import Page

from core.base_page import BasePage
from locator.mobile.login_page_locator import MobileLoginPageLocator


class MobileLoginPage(BasePage):
    """Amazon sign-in page object for mobile web.

    Key differences from desktop:
    - No hover flyout to reach sign-in; click the account link directly.
    - The email input on mobile uses #ap_email (not #ap_email_login).
    """

    @property
    def account_nav_link(self): return self.page.locator(MobileLoginPageLocator.ACCOUNT_NAV_LINK)

    @property
    def email_input(self): return self.page.locator(MobileLoginPageLocator.EMAIL_INPUT)

    @property
    def continue_button(self): return self.page.locator(MobileLoginPageLocator.CONTINUE_BUTTON)

    @property
    def password_input(self): return self.page.locator(MobileLoginPageLocator.PASSWORD_INPUT)

    @property
    def signin_button(self): return self.page.locator(MobileLoginPageLocator.SIGNIN_BUTTON)

    @property
    def error_box(self): return self.page.locator(MobileLoginPageLocator.ERROR_BOX)

    @allure.step("Open Amazon sign-in page via homepage (mobile)")
    def open(self) -> "MobileLoginPage":
        self.navigate("/")
        # Mobile: no hover flyout — click account nav link to go directly to sign-in
        self.click(self.account_nav_link, "Account nav link")
        self.expect_visible(self.email_input, "Email input")
        return self

    @allure.step("Enter email '{email}' and continue")
    def enter_email(self, email: str) -> None:
        self.fill(self.email_input, email, "Email")
        self.click(self.continue_button, "Continue")

    @allure.step("Enter password and sign in")
    def enter_password(self, password: str) -> None:
        self.fill(self.password_input, password, "Password")
        self.click(self.signin_button, "Sign In")

    @allure.step("Login with email '{email}'")
    def login(self, email: str, password: str) -> None:
        self.enter_email(email)
        self.expect_visible(self.password_input, "Password field")
        self.enter_password(password)

    def get_error_message(self) -> str:
        self.expect_visible(self.error_box, "Error message box")
        return self.get_text(self.error_box)
