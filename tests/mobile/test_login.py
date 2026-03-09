import allure
import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.helpers import get_test_data


@allure.feature("Authentication")
class TestMobileLogin:

    @allure.story("Sign-in Page Loads on Mobile")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_signin_page_loads(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.expect_visible(login_page.email_input, "Email input")
        login_page.expect_visible(login_page.continue_button, "Continue button")

    @allure.story("Failed Login - Unregistered Email on Mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_unregistered_email_shows_error(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.enter_email("not.a.real.user.xyz123@example.com")

        error = login_page.get_error_message()
        assert error, "Expected an error message for unregistered email"

    @allure.story("Failed Login - Empty Email on Mobile")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_empty_email_shows_error(self, mobile_page):
        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.enter_email("")

        error = login_page.get_error_message()
        assert error, "Expected a validation error for empty email"

    @allure.story("Failed Login - Invalid Password on Mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_invalid_password_shows_error(self, mobile_page):
        user = get_test_data("users.json", "valid_user")

        login_page = LoginPage(mobile_page)
        login_page.open()
        login_page.enter_email(user["email"])
        login_page.expect_visible(login_page.password_input, "Password field")
        login_page.enter_password("WrongPassword123!")

        error = login_page.get_error_message()
        assert error, "Expected an error message for wrong password"
