from playwright.sync_api import Page, expect, Locator
from config.settings import Settings

class BasePage:
    path = "/"

    def __init__(self, page: Page, settings: Settings):
        self.page, self.settings = page, settings

    @property
    def anchor(self) -> Locator:
        raise NotImplementedError
    
    def open(self):
        self.page.goto(f"{self.settings.base_url}{self.path}")
        expect(self.anchor).to_be_visible()
        return self