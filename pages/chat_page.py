from playwright.sync_api import Locator, expect
from pages.base_page import BasePage
from pages.components.message_thread import MessagesThread

class ChatPage(BasePage):

    @property
    def thread(self) -> MessagesThread:
        return MessagesThread(self.page)
    
    @property
    def chat_input_field(self) -> Locator:
        return self.page.locator("#chat-input")
    
    @property
    def send_button(self) -> Locator:
        return self.page.locator("#send-message-button")
    
    @property
    def stop_button(self) -> Locator:
        """Offered only while the model is streaming; disappears when it finishes."""
        return self.page.get_by_role("button", name="Stop")

    @property
    def model_button(self) -> Locator:
        return self.page.locator("#model-selector-model-button")

    @property
    def new_chat_button(self) -> Locator:
        return self.page.locator("#new-chat-button")

    @property
    def anchor(self) -> Locator:
        return self.chat_input_field

    
    