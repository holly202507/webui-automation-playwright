import allure
from playwright.sync_api import Page

from core.base_page import BasePage


class SearchResultsPage(BasePage):
    """Amazon search results page object."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.results = page.locator("[data-component-type='s-search-result']")
        self.result_titles = page.locator("h2 .a-link-normal .a-text-normal")
        self.total_results_label = page.locator(".a-section .a-color-state")
        self.no_results_message = page.locator(".s-no-outline")
        self.search_input = page.locator("#twotabsearchtab")

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
        self.results.nth(index).locator("h2 a").click()

    def results_contain_keyword(self, keyword: str) -> bool:
        titles = self.get_result_titles()
        return any(keyword.lower() in t.lower() for t in titles)
