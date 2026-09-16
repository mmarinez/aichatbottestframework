"""Behaviour of the chat product: auth, model pinning, answering, context.

Split by cost on purpose. The unmarked tests are fast and deterministic and can
run on every commit; anything marked `llm` spends a real model turn.
"""

import pytest

from pages.chat_page import ChatPage
from pages.login_page import LoginPage


def test_browser_context_is_configured(page):
    """Framework guard: proves the browser_context_args override reaches the page."""
    assert page.viewport_size == {"width": 1920, "height": 1080}


def test_sign_in_lands_on_chat(login_page: LoginPage):
    chat = login_page.sign_in_as_default_user()
    assert chat.is_displayed()


def test_model_under_test_is_pinned(chat_page: ChatPage, settings):
    """Guards the hidden state: the account remembers the last model chosen."""
    assert settings.model in chat_page.selected_model


@pytest.mark.llm
def test_answer_addresses_the_prompt(chat_page: ChatPage):
    answer = chat_page.ask("I like horror movies. What do you recommend this weekend?")

    assert answer, "the assistant returned an empty answer"
    assert "horror" in answer.lower(), f"answer ignored the topic: {answer[:200]!r}"


@pytest.mark.llm
def test_conversation_keeps_context_across_turns(chat_page: ChatPage):
    chat_page.ask("My favourite film genre is horror. Remember that.")
    answer = chat_page.ask("What is my favourite film genre? Answer in one word.")

    thread = chat_page.thread
    assert thread.user_count == 2
    assert thread.assistant_count == 2, f"turns out of sync: {thread.all_answers}"
    assert "horror" in answer.lower(), f"context was lost: {answer[:200]!r}"


@pytest.mark.llm
def test_new_chat_clears_the_thread(chat_page: ChatPage):
    chat_page.ask("Say hello.")
    assert not chat_page.thread.is_empty

    chat_page.new_chat()
    assert chat_page.thread.is_empty
