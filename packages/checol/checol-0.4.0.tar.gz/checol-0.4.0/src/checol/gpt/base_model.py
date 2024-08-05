from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self, api_key, model, max_tokens, system):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.system = system
        self.messages = []

    @abstractmethod
    def send(self, message):
        pass
