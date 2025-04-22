from openai import OpenAI

class Model:
    def __init__(self, model_name: str, client_api: OpenAI):
        self.model_name = model_name
        self.client_api = client_api

    def query(self, msgs: list[object]) -> str:
        """
        Query the model with a given list of messages.
        :param messages: All the exchanges messages. """
        # Call the OpenAI API to get the response
        response = self.client_api.chat.completions.create(
            model=self.model_name,
            messages=msgs
        )
        print(f"{response}")
        return ""

    def __str__(self):
        return f"Model Name: {self.model_name}"