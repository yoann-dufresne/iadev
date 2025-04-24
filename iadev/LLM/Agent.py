from collections import namedtuple
from typing import Optional
import yaml

from iadev.LLM.Model import Model

Message = namedtuple("Message", ["role", "content"])

class Agent:
    def __init__(self, name, model: Model, behavior: Optional[str]=None):
        self.name = name
        self.model = model
        self.messages = [] if behavior is None else [{"role": "system", "content": behavior}]

    def ask(self, content: str) -> str:
        """
        Ask a question to the agent.
        :param content: The content of the question.
        :return: The agent's response. """
        self.add_message(content)
        return self.query()

    def add_message(self, content: str):
        """
        Add a user message to the conversation.
        :param content: The content of the message. """
        self.messages.append(Message("user", content))

    def add_message_with_role(self, role: str, content: str):
        """
        Add a message to the conversation.
        :param role: The role of the message sender (e.g., "user", "assistant").
        :param content: The content of the message. """
        self.messages.append(Message(role, content))

    def query(self) -> str:
        """
        Query the model with the current conversation messages.
        :return: The model's response. """
        message, usage = self.model.query(self.messages)
        self.add_message_with_role(Message(answer["role"], answer["content"]))

    