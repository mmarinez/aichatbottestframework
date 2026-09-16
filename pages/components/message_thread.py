from playwright.sync_api import Locator, Page


class MessagesThread:
    """Read-only view over the conversation transcript.

    A component object, not a page object: it owns a subtree of the DOM, has no
    navigation and no timing logic. `ChatPage` decides *when* to read; this class
    only knows *how* to read.
    """

    ROOT = "#messages-container"
    ASSISTANT = ".chat-assistant"
    USER = ".chat-user"
    # Open WebUI renders user messages with this class too, so it must always be
    # scoped to an assistant bubble — otherwise "the answer" can be your prompt.
    TEXT = ".markdown-prose"

    def __init__(self, page: Page) -> None:
        self.page = page

    # --- locators --------------------------------------------------------
    @property
    def root(self) -> Locator:
        return self.page.locator(self.ROOT)

    @property
    def assistant_messages(self) -> Locator:
        return self.root.locator(self.ASSISTANT)

    @property
    def user_messages(self) -> Locator:
        return self.root.locator(self.USER)

    @property
    def answers(self) -> Locator:
        """Every assistant text block in the thread (one bubble may hold several)."""
        return self.assistant_messages.locator(self.TEXT)

    # --- state -----------------------------------------------------------
    @property
    def assistant_count(self) -> int:
        return self.assistant_messages.count()

    @property
    def user_count(self) -> int:
        return self.user_messages.count()

    @property
    def is_empty(self) -> bool:
        return self.assistant_count == 0

    @property
    def last_answer(self) -> str:
        """Text of the most recent assistant turn.

        Returns "" while the bubble exists but has not streamed any text yet —
        callers poll on that rather than getting a locator timeout.
        """
        if self.is_empty:
            raise AssertionError("no assistant message in the thread yet")
        return self._text_of(self.assistant_messages.last)

    @property
    def all_answers(self) -> list[str]:
        return [
            self._text_of(self.assistant_messages.nth(i))
            for i in range(self.assistant_count)
        ]

    # --- internals -------------------------------------------------------
    @staticmethod
    def _text_of(bubble: Locator) -> str:
        """Join a bubble's text blocks; a single answer can render more than one."""
        blocks = bubble.locator(MessagesThread.TEXT).all_inner_texts()
        return "\n\n".join(block.strip() for block in blocks).strip()
