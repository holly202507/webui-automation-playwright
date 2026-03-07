# UI Test Automation Framework

A reusable, scalable web UI test automation framework built with **Playwright**, **pytest**, and **Allure**.

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.12+ | Language |
| Playwright | Browser automation |
| pytest | Test runner |
| pytest-xdist | Parallel execution |
| Allure | Reporting |
| GitHub Actions | CI/CD |

## Project Structure

```
testing/
├── .github/workflows/    # GitHub Actions CI/CD pipeline
├── core/
│   ├── base_page.py      # BasePage: shared actions & Allure step wrappers
│   └── config.py         # Singleton config loader (config.yaml + env vars)
├── pages/                # Page Objects — one per page or major component
├── tests/                # Test suites
├── data/                 # Test data (JSON)
├── utils/                # Helper functions
├── reports/              # Generated reports (gitignored)
├── conftest.py           # Shared fixtures (browser setup, screenshot on failure)
├── config.yaml           # Environment & browser configuration
├── pytest.ini            # pytest settings and custom markers
└── requirements.txt      # Python dependencies
```

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

```bash
# All tests
pytest

# Specific marker
pytest -m smoke
pytest -m regression

# Specific browser
pytest --browser firefox

# Parallel execution
pytest -n auto

# Headed mode (visible browser)
HEADLESS=false pytest

# Slow motion for debugging
SLOW_MO=500 HEADLESS=false pytest
```

## Allure Reports

```bash
# Run tests and generate results
pytest --alluredir=reports/allure-results

# Serve the report locally
allure serve reports/allure-results
```

## Adding a New Page

1. Create `pages/my_page.py` extending `BasePage`
2. Define locators in `__init__`
3. Add action methods decorated with `@allure.step`
4. Write tests in `tests/test_my_feature.py`

No changes needed to `core/` — it stays reusable across projects.

## Adapting to a New Website

1. Update `config.yaml` with the new site's URLs
2. Add new page objects in `pages/`
3. Add new test data in `data/`
4. Write tests in `tests/`

The `core/` layer is fully reusable and requires no modification.
