import allure
import pytest

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.helpers import get_test_data


@allure.feature("Search")
class TestMobileSearch:

    @allure.story("Homepage Loads on Mobile")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_homepage_loads(self, mobile_page):
        home_page = HomePage(mobile_page)
        home_page.open()
        home_page.verify_loaded()

    @allure.story("Search Returns Results on Mobile")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.mobile
    @pytest.mark.smoke
    @pytest.mark.parametrize("term", get_test_data("search_terms.json", "valid_searches"))
    def test_search_returns_results(self, mobile_page, term):
        home_page = HomePage(mobile_page)
        home_page.open()
        home_page.search(term)

        results_page = SearchResultsPage(mobile_page)
        results_page.verify_loaded()
        assert results_page.get_result_count() > 0, f"Expected results for '{term}'"

    @allure.story("Search Results Relevant to Keyword on Mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_search_results_match_keyword(self, mobile_page):
        term = "laptop"

        home_page = HomePage(mobile_page)
        home_page.open()
        home_page.search(term)

        results_page = SearchResultsPage(mobile_page)
        results_page.verify_loaded()
        assert results_page.results_contain_keyword(term), (
            f"Expected at least one result title to contain '{term}'"
        )

    @allure.story("Clicking Result Opens Product Page on Mobile")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_clicking_result_opens_product_page(self, mobile_page):
        home_page = HomePage(mobile_page)
        home_page.open()
        home_page.search("headphones")

        results_page = SearchResultsPage(mobile_page)
        results_page.verify_loaded()
        results_page.click_result(0)

        results_page.expect_url_contains("/dp/")
