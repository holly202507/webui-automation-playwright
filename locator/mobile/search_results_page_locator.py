class MobileSearchResultsPageLocator:
    RESULTS = "[data-component-type='s-search-result']"
    RESULT_TITLES = (
        "h2 .a-link-normal .a-size-base-plus, "
        "h2 .a-link-normal .a-text-normal"
    )
    NO_RESULTS_MESSAGE = ".s-no-outline"
    SEARCH_INPUT = "#twotabsearchtab"
    RESULT_LINK = "h2 a"
