import pytest
import time
import itertools
from config.settings import Settings, CAPTURES
from pages.chat_page import ChatPage
from pages.login_page import LoginPage
from playwright.sync_api import expect
from evaluators.recorder import Recorder
from collections.abc import Iterator

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

@pytest.fixture
def chat_page(login_page: LoginPage, settings: Settings) -> ChatPage:
    """Signed in, with the model under test pinned.

    Pinning is not cosmetic: Open WebUI remembers the last model this account
    used, so without it the suite grades whichever model was clicked last.
    """
    return login_page.sign_in_as_default_user().select_model(settings.model)

@pytest.fixture(scope="session", autouse=True)
def configure_expect_timeout(settings: Settings):
    expect.set_options(timeout=settings.expect_timeout_ms)

@pytest.fixture
def ask(chat_page, recorder, request):
    counter = itertools.count(1)
    def _ask(prompt: str) -> str:
        t0 = time.perf_counter()
        answer = chat_page.ask(prompt)
        recorder.record(
            capture_id=f"{request.node.name}-{next(counter)}",
            prompt=prompt, 
            response=answer,
            model=chat_page.selected_model,
            duration_ms=int((time.perf_counter() - t0) * 1000),
            test_id=request.node.nodeid,
        )
        return answer
    return _ask

@pytest.fixture(scope="session")
def recorder() -> Iterator[Recorder]:
    rec = Recorder(CAPTURES / "latest.jsonl")
    yield rec
    rec.export_cases(CAPTURES / "cases.json")