import pytest
from config.settings import Settings
from pages.login_page import LoginPage
from playwright.sync_api import expect

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport" : {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "locale": "en-US"

    }

@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.from_env()

@pytest.fixture(scope="session")
def base_url(settings: Settings) -> str:
    return settings.base_url

@pytest.fixture
def login_page(page, settings) -> LoginPage:
    return LoginPage(page, settings).open()

@pytest.fixture(scope="session", autouse=True)
def configure_expect_timeout(settings: Settings):
    expect.set_options(timeout=settings.expect_timeout_ms)