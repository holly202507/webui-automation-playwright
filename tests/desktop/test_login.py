import allure
import pytest

from pageobject.desktop.home_page import HomePage
from pageobject.desktop.login_page import LoginPage
from utils.helpers import get_test_data

# NOTE: Amazon actively detects automated login attempts and may present
# CAPTCHA challenges, especially in headless/CI mode. These tests are
# designed to verify the sign-in flow and error handling. For tests
# requiring an authenticated session, use Playwright's storageState to
# reuse a saved login session instead of logging in each time.


@allure.feature("Authentication")
class TestLogin:

    @allure.story("Sign-in Page Loads")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_signin_page_loads(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.expect_visible(login_page.email_input, "Email input")
        login_page.expect_visible(login_page.continue_button, "Continue button")

    @allure.story("Successful Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_valid_login(self, page):
        user = get_test_data("users.json", "valid_user")

        login_page = LoginPage(page)
        login_page.open()
        login_page.login(user["email"], user["password"])

        home_page = HomePage(page)
        account_label = home_page.get_account_label()
        assert user["display_name"].lower() in account_label.lower(), (
            f"Expected '{user['display_name']}' in account label, got: '{account_label}'"
        )

    @allure.story("Failed Login - Invalid Password")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_invalid_password_shows_error(self, page):
        user = get_test_data("users.json", "valid_user")

        login_page = LoginPage(page)
        login_page.open()
        login_page.enter_email(user["email"])
        login_page.expect_visible(login_page.password_input, "Password field")
        login_page.enter_password("WrongPassword123!")

        error = login_page.get_error_message()
        assert error, "Expected an error message for wrong password"

    @allure.story("Failed Login - Unregistered Email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_unregistered_email_shows_error(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.enter_email("not.a.real.user.xyz123@example.com")

        error = login_page.get_error_message()
        assert error, "Expected an error message for unregistered email"

    @allure.story("Failed Login - Empty Email")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_empty_email_shows_error(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.enter_email("")

        error = login_page.get_error_message()
        assert error, "Expected a validation error for empty email"
