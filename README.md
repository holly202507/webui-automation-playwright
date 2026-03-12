# UI Test Automation Framework (Playwright)

A reusable, scalable web UI test automation framework built with **Playwright**, **pytest**, and **Allure**. Supports **desktop** and **mobile web emulation** testing across Chrome, Firefox, and Safari.

> Real iOS Safari testing (Appium + BrowserStack) lives in the sibling [`../mobile-ui-automation-appium/`](../mobile-ui-automation-appium/) project.

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12+ | Language |
| Playwright | Browser automation (desktop + mobile emulation) |
| pytest | Test runner |
| pytest-xdist | Parallel execution |
| Allure | Reporting |
| GitHub Actions | CI/CD |

## Project Structure

```
web-ui-automation-playwright/
├── .github/workflows/         # GitHub Actions CI/CD pipeline
├── core/
│   ├── base_page.py           # BasePage: Playwright actions & Allure step wrappers
│   └── config.py              # Singleton config loader (config.yaml + env vars)
├── utils/
│   └── helpers.py             # get_test_data() — unified JSON data loader
├── data/                      # Test data (JSON)
├── devices/
│   └── devices.yaml           # Playwright device profiles (iOS + Android)
├── locator/                   # Locator constants — one directory per platform
│   ├── desktop/
│   └── mobile/
├── pageobject/                # Page objects — one directory per platform
│   ├── desktop/               # Desktop page objects
│   └── mobile/                # Mobile emulation page objects
├── tests/                     # Test suites
│   ├── desktop/               # Desktop tests
│   └── mobile/                # Mobile emulation tests
│       └── conftest.py        # mobile_page fixture
├── conftest.py                # Root fixtures (browser setup, screenshot on failure)
├── config.yaml                # Environment and browser configuration
├── pytest.ini                 # pytest settings, markers, and pythonpath
└── requirements.txt           # Python dependencies
```

## Page Object Architecture

Desktop and mobile page objects are fully independent — no cross-platform inheritance. Each platform inherits from `core/BasePage`:

```
core/BasePage  (Playwright)
├── pageobject/desktop/HomePage
├── pageobject/desktop/LoginPage
├── pageobject/desktop/SearchResultsPage
├── pageobject/mobile/MobileHomePage
├── pageobject/mobile/MobileLoginPage
└── pageobject/mobile/MobileSearchResultsPage
```

This ensures desktop and mobile locators are fully isolated — a DOM change on one platform cannot break the other.

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install --with-deps
```

## Configuration

Edit `config.yaml` to set your target URLs:

```yaml
environments:
  dev:
    base_url: "https://your-dev-site.com"
  staging:
    base_url: "https://your-staging-site.com"
```

Override at runtime with environment variables:

```bash
TEST_ENV=staging BASE_URL=https://override.com pytest
```

## Running Tests

### Desktop

```bash
# All desktop tests
pytest tests/desktop/

# By marker
pytest tests/desktop/ -m smoke
pytest tests/desktop/ -m regression

# Specific browser
pytest tests/desktop/ --browser firefox

# Parallel execution
pytest tests/desktop/ -n auto

# Headed mode with slow motion (debugging)
HEADLESS=false SLOW_MO=500 pytest tests/desktop/
```

### Mobile (Playwright Emulation)

Device profiles are defined in `devices/devices.yaml`.

```bash
# Default device (iPhone 14)
pytest tests/mobile/ -m mobile

# Specific device
pytest tests/mobile/ --mobile-device samsung_galaxy_s23
pytest tests/mobile/ --mobile-device pixel_7
```

Available devices:

| Key | Device | Browser |
|-----|--------|---------|
| `iphone_14` | iPhone 14 | WebKit |
| `iphone_14_pro` | iPhone 14 Pro | WebKit |
| `samsung_galaxy_s23` | Samsung Galaxy S23 | Chromium |
| `pixel_7` | Pixel 7 | Chromium |

## CI/CD

| Trigger | Suite |
|---------|-------|
| Every PR | Desktop + mobile emulation smoke |
| Nightly | Full desktop + mobile regression |

Reports are generated with Allure and deployed to GitHub Pages from the `main` branch.

## Allure Reports

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Test Data

All test data lives in `data/` as JSON files:

```python
from utils.helpers import get_test_data

get_test_data("users.json", "valid_user", "email")
get_test_data("search_terms.json", "valid_searches")  # returns a list, usable in parametrize
```

## Adding a New Page

1. Create page objects in the relevant platform directories:
   - `pageobject/desktop/my_page.py` extending `core.base_page.BasePage`
   - `pageobject/mobile/my_page.py` extending `core.base_page.BasePage`
2. Define locators as class attributes and add action methods decorated with `@allure.step`
3. Write tests in `tests/desktop/` and/or `tests/mobile/`
