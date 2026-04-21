# OrangeHRM Interface Automation

Python + Pytest + Playwright + Requests based API automation project for OrangeHRM demo site.

## Tech Stack

- Python
- pytest
- playwright
- requests
- allure-pytest
- pyyaml
- loguru

## Project Structure

```text
OrangeHRM-interface/
├── common/                  # logger and requests client wrapper
├── config/                  # environment config
├── data/                    # test data yaml/json
├── pages/                   # API object encapsulation
├── tests/                   # test cases
├── logs/                    # runtime logs
├── conftest.py              # global fixtures (login + api session)
├── pytest.ini               # pytest config
├── requirements.txt         # dependencies
└── README.md
```

## Environment Setup

Use PowerShell under project root:

```powershell
# 1. Create virtual environment (skip if already exists)
python -m venv .venv

# 2. Activate
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r .\requirements.txt

# 4. Install Playwright browser
playwright install chromium
```

## Configuration

Config files:

- `config/config.dev.yaml`
- `config/config.test.yaml`
- `config/config.yaml` (fallback if env-specific file does not exist)

Set values in your target environment file:

- `base_url`: OrangeHRM URL
- `username`: login user
- `password`: login password

## Run Tests

```powershell
# Run all tests
.\.venv\Scripts\python.exe -m pytest -s

# Run against test env config
.\.venv\Scripts\python.exe -m pytest -s --env=test

# Run employee management test only
.\.venv\Scripts\python.exe -m pytest -q tests/test_employee_management.py -s

# Run by markers
.\.venv\Scripts\python.exe -m pytest -s -m smoke
.\.venv\Scripts\python.exe -m pytest -s -m pim
```

## Allure Report

`pytest.ini` already includes `--alluredir=./allure-results`.

```powershell
# Generate and open report (requires allure cli)
allure serve .\allure-results
```

## Logging

- Console output: enabled by loguru
- File output: `logs/test.log`

## Current Business Flow

- Login with Playwright headless mode and extract browser cookies
- Inject cookies into `requests.Session`
- Add employee
- Verify employee appears in employee list
- Delete created employee in fixture teardown (cleanup guaranteed)

