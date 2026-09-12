from playwright.sync_api import Page, expect
import time

# def test_polite_tone(login_page):
#     user_input = "I like horror movies, What do you recommend this weekend?"
#     chat = login_page.sign_in_user()
#     answer = chat.ask(user_input)
#     assert "horror" in answer.lower()

def test_context_options(page):
    assert page.viewport_size == {"width": 1920, "height": 1080}

def test_sign_in_lands_on_chat(login_page):
    chat = login_page.sign_in_as_default_user()
    assert chat.is_displayed()
    