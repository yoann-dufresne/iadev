
class Model:
    def __init__(self, model_name: str, server):
        self.model_name = model_name
        self.server = server

    def query(self, msgs: list[object]) -> tuple:
        """
        Query the server with self model and a given list of messages.
        :param messages: All the exchanges messages. """
        return self.server.query_chat(self, msgs)

    def __str__(self):
        return f"Model Name: {self.model_name}"
    