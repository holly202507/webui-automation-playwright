import allure
from playwright.sync_api import Page

from core.base_page import BasePage
from locator.desktop.search_results_page_locator import SearchResultsPageLocator


class SearchResultsPage(BasePage):
    """Amazon search results page object."""

    @property
    def results(self): return self.page.locator(SearchResultsPageLocator.RESULTS)

    @property
    def result_titles(self): return self.page.locator(SearchResultsPageLocator.RESULT_TITLES)

    @property
    def total_results_label(self): return self.page.locator(SearchResultsPageLocator.TOTAL_RESULTS_LABEL)

    @property
    def no_results_message(self): return self.page.locator(SearchResultsPageLocator.NO_RESULTS_MESSAGE)

    @property
    def search_input(self): return self.page.locator(SearchResultsPageLocator.SEARCH_INPUT)

    @allure.step("Verify search results page is loaded")
    def verify_loaded(self) -> "SearchResultsPage":
        self.expect_visible(self.results.first, "First search result")
        return self

    @allure.step("Verify no results message is shown")
    def verify_no_results(self) -> "SearchResultsPage":
        self.expect_visible(self.no_results_message, "No results message")
        return self

    def get_result_count(self) -> int:
        return self.results.count()

    def get_result_titles(self) -> list[str]:
        return self.result_titles.all_inner_texts()

    def get_first_result_title(self) -> str:
        return self.result_titles.first.inner_text()

    @allure.step("Click on result at index {index}")
    def click_result(self, index: int = 0) -> None:
        self.results.nth(index).locator(SearchResultsPageLocator.RESULT_LINK).click()

    def results_contain_keyword(self, keyword: str) -> bool:
        titles = self.get_result_titles()
        return any(keyword.lower() in t.lower() for t in titles)
