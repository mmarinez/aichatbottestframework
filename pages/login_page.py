from playwright.sync_api import Locator
from pages.base_page import BasePage
from pages.chat_page import ChatPage

class LoginPage(BasePage):
    path = "/auth"

    @property
    def email_field(self) -> Locator:
        return self.page.locator("input#email")
    
    @property
    def password_field(self) -> Locator:
        return self.page.locator("input#password")
    
    @property
    def sign_in_button(self) -> Locator:
        return self.page.get_by_role('button', name='Sign in')
    
    @property
    def anchor(self) -> Locator:
        return self.email_field
    
    def sign_in_as_default_user(self):
        self.email_field.fill(self.settings.email)
        self.password_field.fill(self.settings.password)
        self.sign_in_button.click()
        return ChatPage(self.page, self.settings).wait_until_ready()
    