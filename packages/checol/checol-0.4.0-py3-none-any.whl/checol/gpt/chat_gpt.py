from openai import OpenAI
from .base_model import BaseModel


class ChatGPT(BaseModel):
    def __init__(
        self,
        api_key,
        model="gpt-4o-mini",
        max_tokens=1000,
        system="このコード差分を見てプロの目線でコードレビューしてください",
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.messages = [{"role": "system", "content": system}]
        self.client = OpenAI(api_key=api_key)

    def send(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=self.messages
        )

        content = result.choices[0].message.content
        self.messages.append({"role": "assistant", "content": content})
        return content
