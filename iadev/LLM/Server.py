import yaml
from openai import OpenAI
from iadev.LLM.Model import Model
from typing import Dict, List, Optional


class Server:
    def __init__(self) -> None:
        self.client: Optional[OpenAI] = None

    def connect(self) -> None:
        pass

    def get_model_names(self) -> List[str]:
        pass

    def get_model(self, model_name: str) -> Model:
        pass


class PasteurLibreChat(Server):
    def __init__(self) -> None:
        super().__init__()
        self.name: str = "Pasteur Libre Chat"
        self.config: Optional[Dict[str, str]] = load_config("credentials/pasteur_librechat.yaml")
        self.model: Dict[str, Optional[Model]] = {}

    def connect(self) -> None:
        if self.config is None:
            raise ValueError("Configuration could not be loaded.")
        self.client = OpenAI(api_key=self.config['token'], base_url=self.config['server'])
        for model_name in self.get_model_names():
            self.model[model_name] = None

    def get_model_names(self) -> List[str]:
        return ["mistral-small-2503-local",
                "llama3-3-70b-local",
                "gemma-3-27b-local",
                "qwen2-5-14b-coder-local"]

    def get_model(self, model_name: str) -> Model:
        if model_name in self.model:
            if self.model[model_name] is None:
                if self.client is None:
                    raise ValueError("Client is not connected.")
                self.model[model_name] = Model(model_name, self.client)
            return self.model[model_name]
        else:
            raise ValueError(f"Model {model_name} not found.")


def load_config(file_path: str) -> Optional[Dict[str, str]]:
    """
    Loads a YAML config file and returns the data.

    Args:
        file_path: The path to the YAML file.

    Returns:
        A Python dictionary or list representing the YAML data.
        Returns None if an error occurs.
    """
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)  # Use safe_load for security
        return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except yaml.YAMLError as e:
        print(f"YAML Error: {e}")
        return None