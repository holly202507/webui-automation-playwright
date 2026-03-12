import allure
from playwright.sync_api import Page

from core.base_page import BasePage
from locator.desktop.login_page_locator import LoginPageLocator


class LoginPage(BasePage):
    """Amazon sign-in page object.

    Amazon's sign-in flow:
      1. Homepage → hover "Hello, Sign in" account link
      2. Click "Sign in" button from the flyout dropdown
      3. Enter email → click Continue
      4. Enter password → click Sign In

    NOTE: Automated login on Amazon may trigger CAPTCHA or bot-detection,
    especially in headless/CI environments. For tests that require an
    authenticated session, prefer saving browser storage state after a
    one-time manual login (Playwright storageState) rather than logging
    in on every test run.
    """

    @property
    def account_nav_link(self): return self.page.locator(LoginPageLocator.ACCOUNT_NAV_LINK)

    @property
    def flyout_signin_link(self): return self.page.locator(LoginPageLocator.FLYOUT_SIGNIN_LINK).first

    @property
    def email_input(self): return self.page.locator(LoginPageLocator.EMAIL_INPUT)

    @property
    def continue_button(self): return self.page.locator(LoginPageLocator.CONTINUE_BUTTON)

    @property
    def password_input(self): return self.page.locator(LoginPageLocator.PASSWORD_INPUT)

    @property
    def signin_button(self): return self.page.locator(LoginPageLocator.SIGNIN_BUTTON)

    @property
    def error_box(self): return self.page.locator(LoginPageLocator.ERROR_BOX)

    @allure.step("Open Amazon sign-in page via homepage")
    def open(self) -> "LoginPage":
        self.navigate("/")
        self.hover(self.account_nav_link, "Hello, Sign in")
        self.expect_visible(self.flyout_signin_link, "Sign in flyout button")
        self.click(self.flyout_signin_link, "Sign in flyout button")
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
