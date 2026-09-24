from ollama import chat
from ollama import ChatResponse


def call_api(prompt: str, options: dict, context: dict):
    response: ChatResponse = chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI movie theather assistant. "
                    "Your role is to suggest movies."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return {
        "output": response.message.content
    }