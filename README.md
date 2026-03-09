# UI Test Automation Framework

A reusable, scalable web UI test automation framework built with **Playwright**, **pytest**, and **Allure**. Supports both **desktop** and **mobile web** testing across Chrome, Firefox, Safari, iOS, and Android.

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12+ | Language |
| Playwright | Browser automation (desktop + mobile emulation) |
| Appium | Real device testing (iOS Safari nightly) |
| pytest | Test runner |
| pytest-xdist | Parallel execution |
| Allure | Reporting |
| BrowserStack | Cloud device farm |
| GitHub Actions | CI/CD |

## Project Structure

```
webui-automation-playwright/
├── .github/workflows/         # GitHub Actions CI/CD pipeline
├── core/
│   ├── base_page.py           # BasePage: shared actions & Allure step wrappers
│   └── config.py              # Singleton config loader (config.yaml + env vars)
├── pages/                     # Page Objects — shared by desktop and mobile tests
│   ├── home_page.py
│   ├── login_page.py
│   └── search_results_page.py
├── tests/
│   ├── desktop/               # Desktop browser test suites
│   │   ├── test_login.py
│   │   └── test_search.py
│   └── mobile/                # Mobile web test suites
│       ├── conftest.py        # mobile_page (Playwright) + appium_driver fixtures
│       ├── test_login.py
│       └── test_search.py
├── mobile/
│   ├── devices.yaml           # iOS and Android device profiles
│   └── browserstack.yml       # BrowserStack project/build labels
├── data/                      # Test data (JSON)
│   ├── users.json
│   └── search_terms.json
├── utils/
│   └── helpers.py             # get_test_data() — unified JSON data loader
├── reports/                   # Generated reports (gitignored)
├── conftest.py                # Shared fixtures (browser setup, screenshot on failure)
├── config.yaml                # Environment, browser, and mobile configuration
├── pytest.ini                 # pytest settings and custom markers
└── requirements.txt           # Python dependencies
```

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers (includes WebKit for iOS emulation)
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

# Headed mode (visible browser window)
HEADLESS=false pytest tests/desktop/

# Slow motion for debugging
SLOW_MO=500 HEADLESS=false pytest tests/desktop/
```

### Mobile

Mobile tests use Playwright device emulation by default. Device profiles are defined in `mobile/devices.yaml`.

```bash
# Mobile tests — default device (iPhone 14)
pytest tests/mobile/ -m mobile

# Mobile tests — specific device
pytest tests/mobile/ --mobile-device samsung_galaxy_s23
pytest tests/mobile/ --mobile-device pixel_7

# Mobile smoke only
pytest tests/mobile/ -m smoke

# Mobile regression only
pytest tests/mobile/ -m regression
```

Available devices (defined in `mobile/devices.yaml`):

| Key | Device | Browser |
|-----|--------|---------|
| `iphone_14` | iPhone 14 | WebKit (Safari engine) |
| `iphone_14_pro` | iPhone 14 Pro | WebKit (Safari engine) |
| `samsung_galaxy_s23` | Samsung Galaxy S23 | Chromium (Chrome) |
| `pixel_7` | Pixel 7 | Chromium (Chrome) |

### Nightly Real iOS Safari (Appium + BrowserStack)

For real Safari on a real iPhone — catches Safari-specific bugs that emulation may miss.

```bash
# Requires BrowserStack credentials
export BROWSERSTACK_USERNAME=your_username
export BROWSERSTACK_ACCESS_KEY=your_access_key

pytest tests/mobile/ -m safari --mobile-device iphone_14
```

## CI/CD Strategy

| Trigger | Suite | Runner |
|---------|-------|--------|
| Every PR | Desktop + Mobile smoke | Playwright (local/BrowserStack) |
| Nightly | Full regression | Playwright (local/BrowserStack) |
| Nightly | Real iOS Safari smoke | Appium + BrowserStack real device |

## Allure Reports

```bash
# Run tests and generate results
pytest --alluredir=reports/allure-results

# Serve the report locally
allure serve reports/allure-results
```

## Test Data

All test data lives in `data/` as JSON files. Use the unified helper to load any value:

```python
from utils.helpers import get_test_data

# Load a full user dict
get_test_data("users.json", "valid_user")

# Load a specific field
get_test_data("users.json", "valid_user", "email")

# Load a list (used directly in @pytest.mark.parametrize)
get_test_data("search_terms.json", "valid_searches")
```

## Adding a New Page

1. Create `pages/my_page.py` extending `BasePage`
2. Define locators in `__init__`
3. Add action methods decorated with `@allure.step`
4. Write tests in `tests/desktop/test_my_feature.py` and/or `tests/mobile/test_my_feature.py`

The same page object works for both desktop and mobile — no duplication needed.

## Adapting to a New Website

1. Update `config.yaml` with the new site's URLs
2. Add new page objects in `pages/`
3. Add new test data in `data/`
4. Write tests in `tests/desktop/` and `tests/mobile/`

The `core/` layer is fully reusable and requires no modification.
