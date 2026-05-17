import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


class Agent:
    def __init__(self, name, system_prompt, model):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model

    def reply(self, conversation):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        messages.extend(conversation)

        print(f"\n===== {self.name} =====")
        print(messages)

        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": messages
            }
        )

        print("\nSTATUS CODE:")
        print(response.status_code)

        print("\nRAW RESPONSE:")
        print(response.text)

        data = response.json()

        return data["choices"][0]["message"]["content"]