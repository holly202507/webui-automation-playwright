# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt
playwright install

# Run all desktop tests
pytest tests/desktop/

# Run a single test file
pytest tests/desktop/test_search.py

# Run a single test by name
pytest tests/desktop/test_search.py::TestSearch::test_homepage_loads

# Run by marker
pytest -m smoke
pytest -m "regression and mobile"

# Parallel execution
pytest tests/desktop/ -n auto

# Headed mode with slow motion (debugging)
HEADLESS=false SLOW_MO=500 pytest tests/desktop/

# Mobile tests (Playwright emulation, default: iPhone 14)
pytest tests/mobile/ -m mobile
pytest tests/mobile/ -m mobile --mobile-device samsung_galaxy_s23

# Generate and serve Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

> Real iOS Safari (Appium) tests have been moved to the sibling [`../mobile-ui-automation-appium/`](../mobile-ui-automation-appium/) project.

## Architecture

Two parallel page-object hierarchies exist — one per platform. They do **not** share a common base:

| Platform | Base class | Located at |
|---|---|---|
| Desktop (Playwright) | `core/base_page.py` → `BasePage` | `pageobject/desktop/` |
| Mobile emulation (Playwright) | `core/base_page.py` → `BasePage` | `pageobject/mobile/` |

`BasePage` wraps Playwright actions with `@allure.step` decorators and automatic screenshots.

### Configuration

`core/config.py` exposes a global `config` singleton loaded once from `config.yaml`. Environment variables take precedence:

| Env var | Config key | Purpose |
|---|---|---|
| `TEST_ENV` | `default_env` | `dev` / `staging` / `prod` |
| `BASE_URL` | `environments.<env>.base_url` | Override base URL |
| `TIMEOUT` | `environments.<env>.timeout` | Timeout in ms |
| `HEADLESS` | `browser.headless` | Headless toggle |
| `SLOW_MO` | `browser.slow_mo` | Slow motion delay (ms) |

### Test Data

All test data lives in `data/` as JSON. Load it with the helper:

```python
from utils.helpers import get_test_data

email = get_test_data("users.json", "valid_user", "email")
```

### Fixtures

- **Root `conftest.py`**: Handles Playwright browser launch args, `--mobile-device` CLI option, and screenshot-on-failure for desktop/mobile tests.
- **`tests/mobile/conftest.py`**: Provides `mobile_page` (Playwright device emulation) fixture. Device profiles are defined in `devices/devices.yaml`.

### Test Markers

Defined in `pytest.ini`: `smoke`, `regression`, `login`, `mobile`, `ios`, `android`.

### CI/CD

`.github/workflows/ui-tests.yml` runs a browser matrix (chromium, firefox, webkit) on push/PR and deploys Allure reports to GitHub Pages from the `main` branch.
