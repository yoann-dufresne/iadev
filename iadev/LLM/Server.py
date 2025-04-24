import yaml
from openai import OpenAI, InternalServerError
from sys import stderr
from iadev.LLM.Model import Model
from typing import Dict, List, Optional

from iadev.LLM.Agent import Agent, Message

class Server:
    def __init__(self) -> None:
        self.models: Dict[str, Optional[Model]] = {x: None for x in self.get_model_names()}

    def connect(self) -> None:
        pass

    def get_model_names(self) -> List[str]:
        return ["mistral-small-2503",
                "llama3-3-70b",
                "gemma-3-27b",
                "qwen2-5-14b-coder"]

            
    def get_default_model(self) -> Model:
        return self.get_model(self.get_model_names()[0])

    def get_model(self, model_name: str) -> Model:
        pass
    
    def query_chat(self, model: Model, messages: List[tuple]) -> tuple:
        answer = None
        return answer

    def agent_from_yaml(self, yaml_file: str) -> Agent:
        """
        Loads a YAML file and returns the agent object.
        :param yaml_file: The path to the YAML file.
        :return: An Agent object corresponding to the description in the yaml file.
        """
        with open(yaml_file, 'r') as f:
            data = yaml.safe_load(f)
        if "name" not in data:
            raise ValueError("Agent name is required in the YAML file.")
        if "description" not in data:
            raise ValueError("Agent description is required in the YAML file.")
        model = self.get_model(data['model']) if 'model' in data else self.get_default_model()
        agent = Agent(data['name'], model, data['description'])
        return agent


class PasteurLibreChat(Server):
    def __init__(self) -> None:
        super().__init__()
        self.name: str = "Pasteur Libre Chat"
        self.config: Optional[Dict[str, str]] = load_config("credentials/pasteur_librechat.yaml")
        self.models: Dict[str, Optional[Model]] = {}

    def connect(self) -> None:
        if self.config is None:
            raise ValueError("Configuration could not be loaded.")
        self.client = OpenAI(api_key=self.config['token'], base_url=self.config['server'])
        for model_name in self.get_model_names():
            self.models[model_name] = None
    
    def get_default_model(self) -> Model:
        return self.get_model("mistral-small-2503")

    def get_model(self, model_name: str) -> Model:
        if model_name in self.models:
            if self.models[model_name] is None:
                if self.client is None:
                    raise ValueError("Client is not connected.")
                self.models[model_name] = Model(f"{model_name}-local", self)
            return self.models[model_name]
        else:
            raise ValueError(f"Model {model_name} not found.")
        
    def query_chat(self, model: Model, messages: List[Message]) -> tuple[Message, object]:
        api_messages = [{"role": message.role, "content": message.content} for message in messages]
        try:
            response = self.client.chat.completions.create(
                model=model.model_name,
                messages=api_messages
            )
            
            num_responses = len(response.choices)
            if num_responses == 0:
                raise ValueError("No response from the server.")
            elif num_responses > 1:
                print("Multiple responses received. Returning the first one.", file=stderr)
            answer = response.choices[0]
            return Message(answer['role'], answer['content']), response.usage['total_tokens']
        except InternalServerError as e:
            print(e, file=stderr)
        return None, None

class OllamaLocal(Server):
    def __init__(self) -> None:
        super().__init__()
        self.name: str = "Ollama Local"
        self.config: Optional[Dict[str, str]] = load_config("credentials/ollama.yaml")

    def connect(self) -> None:
        if self.config is None:
            raise ValueError("Configuration could not be loaded.")
        self.client = OpenAI(api_key="ollama", base_url=self.config['server'])
        for model_name in self.get_model_names():
            self.models[model_name] = None

    def get_model_names(self) -> List[str]:
        return ["llama3.2"]

    def get_model(self, model_name: str) -> Model:
        if model_name in self.models:
            return None
        else:
            raise ValueError(f"Model {model_name} not found.")
        
    def query_chat(self, model, messages):
        raise NotImplementedError("Ollama Local server does not support chat completions.")
        try:
            response = self.client.chat.completions.create(
                model=model.model_name,
                messages=messages
            )
            print(response)
        except InternalServerError as e:
            print(e, file=stderr)
        return None

def load_config(file_path: str) -> Dict[str, str]:
    """
    Loads a YAML config file and returns the data.

    Args:
        file_path: The path to the YAML file.

    Returns:
        A Python dictionary or list representing the YAML data.
        Returns None if an error occurs.
    """
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)  # Use safe_load for security
    return data