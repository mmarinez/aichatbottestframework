from playwright.sync_api import Locator
from pages.base_page import BasePage
from pages.components.message_thread import MessagesThread

class ChatPage(BasePage):

    @property
    def thread(self) -> MessagesThread:
        return MessagesThread(self.page)