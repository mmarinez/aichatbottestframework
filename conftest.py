import pytest
from config.settings import Settings

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport" : {"width": 1920, "height": 1080},
        "ignore_https_error": True,
        "locale": "en-US"

    }

@pytest.fixture(scope="session")
def base_url(settings: Settings) -> str:
    return settings.base_url