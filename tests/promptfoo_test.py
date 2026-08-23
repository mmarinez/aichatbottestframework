from playwright.sync_api import Page, expect
import time

def test_polite_tone(page: Page):
    user_input = "I like horror movies, What do you recommend this weekend?"
    page.goto("http://localhost:3000/")

    user_email = page.locator("input[id=email]")
    user_password = page.locator("input[id=password]")
    sign_in_button = page.locator("div[class=self-center]")

    user_email.fill("marinezbay94@gmail.com")
    user_password.fill("Madriguez94")
    sign_in_button.click()

    ollama_input_field = page.locator("div[id=chat-input]")
    ollama_send_message_button = page.locator("button[id=send-message-button]")
    ollama_input_field.fill(user_input)
    ollama_send_message_button.click()
    time.sleep(15)


    