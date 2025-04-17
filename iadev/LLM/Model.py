from openai import OpenAI

class Model:
    def __init__(self, model_name: str, client_api: OpenAI):
        self.model_name = model_name
        self.client_api = client_api

    def query(self, prompt: str) -> str:
        """
        Query the model with a given prompt.
        :param prompt: The prompt to send to the model. """
        response = self.client_api.Completion.create(
            model=self.model_name,
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def __str__(self):
        return f"Model Name: {self.model_name}"