import time

from playwright.sync_api import Locator, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage
from pages.components.message_thread import MessagesThread


class ChatPage(BasePage):
    # How often to re-read the streaming answer, and how many identical reads
    # in a row mean "the model has stopped typing".
    POLL_MS = 750
    STABLE_SAMPLES = 2

    @property
    def thread(self) -> MessagesThread:
        return MessagesThread(self.page)

    # --- locators --------------------------------------------------------
    @property
    def chat_input_field(self) -> Locator:
        return self.page.locator("#chat-input")

    @property
    def send_button(self) -> Locator:
        """Only rendered once the input is non-empty."""
        return self.page.locator("#send-message-button")

    @property
    def stop_button(self) -> Locator:
        """Visible while *any* generation runs — including the follow-up title
        and tag requests Open WebUI fires after the answer. Useful for "is it
        busy", useless as a completion signal."""
        return self.page.get_by_role("button", name="Stop")

    @property
    def model_button(self) -> Locator:
        return self.page.locator("#model-selector-model-button")

    @property
    def model_search_box(self) -> Locator:
        return self.page.get_by_placeholder("Search a model")

    @property
    def model_options(self) -> Locator:
        return self.page.locator("[role=option]")

    @property
    def new_chat_button(self) -> Locator:
        return self.page.locator("#new-chat-button")

    @property
    def anchor(self) -> Locator:
        return self.chat_input_field

    # --- state -----------------------------------------------------------
    @property
    def selected_model(self) -> str:
        return self.model_button.inner_text().strip()

    # --- actions ---------------------------------------------------------
    def select_model(self, name: str) -> "ChatPage":
        """Pin the model under test.

        Open WebUI remembers the last model chosen by this account, so without
        this the suite grades whichever model someone last clicked.
        """
        if name in self.selected_model:
            return self
        self.model_button.click()
        self.model_search_box.fill(name)
        expect(self.model_options.first).to_be_visible()
        self.model_options.first.click()
        expect(self.model_button).to_contain_text(name)
        return self

    def send(self, prompt: str) -> "ChatPage":
        self._wait_until_idle()
        self.chat_input_field.fill(prompt)
        expect(self.send_button).to_be_enabled()
        self.send_button.click()
        return self

    def ask(self, prompt: str, timeout_ms: int | None = None) -> str:
        """Send a prompt and return the assistant's completed answer."""
        expected_count = self.thread.assistant_count + 1
        self.send(prompt)
        return self.wait_for_answer(expected_count, timeout_ms)

    def wait_for_answer(self, expected_count: int, timeout_ms: int | None = None) -> str:
        """Wait for the streamed answer to arrive and stop changing.

        Text stability rather than a control's state: the answer is the thing
        being measured, so it is also the most reliable thing to wait on.
        """
        timeout_ms = timeout_ms or self.settings.response_timeout_ms
        expect(self.thread.assistant_messages).to_have_count(
            expected_count, timeout=timeout_ms
        )

        deadline = time.monotonic() + timeout_ms / 1000
        previous, stable = "", 0
        while time.monotonic() < deadline:
            self.page.wait_for_timeout(self.POLL_MS)
            current = self.thread.last_answer
            if current and current == previous:
                stable += 1
                if stable >= self.STABLE_SAMPLES:
                    return current
            else:
                stable = 0
            previous = current

        raise AssertionError(
            f"answer did not settle within {timeout_ms} ms. "
            f"Last text seen: {previous[:200]!r}"
        )

    def new_chat(self) -> "ChatPage":
        if self.new_chat_button.is_visible():
            self.new_chat_button.click()
        else:
            self.open()
        expect(self.thread.assistant_messages).to_have_count(0)
        return self

    # --- internals -------------------------------------------------------
    def _wait_until_idle(self, timeout_ms: int = 3_000) -> None:
        """Best effort: avoid typing while a previous generation is in flight.

        Open WebUI's post-answer requests can keep Stop visible indefinitely, so
        a timeout here is not a failure.
        """
        try:
            self.stop_button.wait_for(state="hidden", timeout=timeout_ms)
        except PlaywrightTimeoutError:
            pass
