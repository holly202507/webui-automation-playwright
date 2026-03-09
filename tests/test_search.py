import allure
import pytest

from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.helpers import get_test_data


@allure.feature("Search")
class TestSearch:

    @allure.story("Homepage Loads")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_homepage_loads(self, page):
        home_page = HomePage(page)
        home_page.open()
        home_page.verify_loaded()

    @allure.story("Search Returns Results")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("term", get_test_data("search_terms.json", "valid_searches"))
    def test_search_returns_results(self, page, term):
        home_page = HomePage(page)
        home_page.open()
        home_page.search(term)

        results_page = SearchResultsPage(page)
        results_page.verify_loaded()
        assert results_page.get_result_count() > 0, f"Expected results for '{term}'"

    @allure.story("Search Results Relevant to Keyword")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_search_results_match_keyword(self, page):
        term = "laptop"

        home_page = HomePage(page)
        home_page.open()
        home_page.search(term)

        results_page = SearchResultsPage(page)
        results_page.verify_loaded()
        assert results_page.results_contain_keyword(term), (
            f"Expected at least one result title to contain '{term}'"
        )

    @allure.story("Search from Data File")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_search_terms_from_data(self, page):
        home_page = HomePage(page)
        results_page = SearchResultsPage(page)

        for term in get_test_data("search_terms.json", "valid_searches"):
            with allure.step(f"Search for '{term}'"):
                home_page.open()
                home_page.search(term)
                results_page.verify_loaded()

    @allure.story("Empty Search")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_empty_search_stays_on_homepage(self, page):
        home_page = HomePage(page)
        home_page.open()
        home_page.search("")
        # Amazon redirects to a results/browse page on empty search
        # Verify we are still on amazon.com domain
        home_page.expect_url_contains("amazon.com")

    @allure.story("Search Result Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_clicking_result_opens_product_page(self, page):
        home_page = HomePage(page)
        home_page.open()
        home_page.search("headphones")

        results_page = SearchResultsPage(page)
        results_page.verify_loaded()
        results_page.click_result(0)

        # Product pages contain /dp/ in the URL
        results_page.expect_url_contains("/dp/")
