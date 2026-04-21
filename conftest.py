from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

from common.logger import log
from common.rest_client import RestClient
from pages.employee_api import EmployeeApi


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Target environment for config file. Uses config/config.<env>.yaml",
    )


def _load_config(env: str) -> dict[str, Any]:
    cfg_path = Path(__file__).parent / "config" / f"config.{env}.yaml"
    if not cfg_path.exists():
        cfg_path = Path(__file__).parent / "config" / "config.yaml"
    with cfg_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@pytest.fixture(scope="session")
def api_session(request: pytest.FixtureRequest) -> RestClient:
    """
    Use Playwright to login (headless) and reuse cookies in requests.Session.
    """
    env = request.config.getoption("--env")
    cfg = _load_config(env).get("orangehrm", {})
    base_url = str(cfg.get("base_url", "")).rstrip("/") + "/"
    username = cfg.get("username", "")
    password = cfg.get("password", "")

    client = RestClient(base_url=base_url, default_timeout=30)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        login_url = base_url + "web/index.php/auth/login"
        log.info("Playwright login -> {url}", url=login_url)
        page.goto(login_url, wait_until="domcontentloaded")

        page.locator("input[name='username']").fill(username)
        page.locator("input[name='password']").fill(password)
        page.locator("button[type='submit']").click()

        try:
            page.wait_for_url("**/web/index.php/dashboard/**", timeout=30_000)
        except PlaywrightTimeoutError as exc:
            current_url = page.url
            page_title = page.title()
            raise RuntimeError(
                f"Login failed or timeout. current_url={current_url}, title={page_title}"
            ) from exc

        cookies = context.cookies()
        if not cookies:
            raise RuntimeError("Login finished but no cookies found in browser context.")
        log.info("Login ok, cookies={count}", count=len(cookies))

        for c in cookies:
            name = c.get("name")
            value = c.get("value")
            domain = c.get("domain")
            path = c.get("path") or "/"
            if name and value:
                client.session.cookies.set(name, value, domain=domain, path=path)

        context.close()
        browser.close()

    return client


@pytest.fixture(scope="session")
def employee_api(api_session: RestClient, request: pytest.FixtureRequest) -> EmployeeApi:
    env = request.config.getoption("--env")
    cfg = _load_config(env).get("orangehrm", {})
    base_url = str(cfg.get("base_url", "")).rstrip("/") + "/"
    return EmployeeApi(api_session, base_url)

