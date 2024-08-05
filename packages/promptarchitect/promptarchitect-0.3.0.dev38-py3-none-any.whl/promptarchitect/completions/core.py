import json
import logging
from pathlib import Path

import coloredlogs

# Configuring logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
coloredlogs.install(level="INFO")


class Completion:
    """
    Abstract base class for completions.
    """

    def __init__(
        self, system_role: str, model: str, parameters: dict, pricing_file: str
    ):
        """
        Initialize the CompletionBase class with necessary configuration.

        Args:
            system_role (str): The role assigned to the system in the conversation.
            model (str): The model used for the API calls.
            parameters (dict): Additional parameters for the completion request.
            pricing_file (str): Path to the pricing file.
        """

        price_file_path = Path(__file__).parent.parent / "pricing" / pricing_file

        with open(price_file_path, "r") as config_pricing_file:
            self.pricing = json.load(config_pricing_file)

        if model not in self.pricing.keys():
            raise ValueError(
                f"Model {model} not supported. Check the pricing file {pricing_file}."
            )

        self.system_role = system_role
        self.model = model
        self._prompt = ""
        self.parameters = parameters
        self.cost = 0.0
        self.is_json = False
        self.test_path = ""
        self.response_message = ""
        self.latency = 0.0

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate the cost of the completion based on the number of tokens.

        Args:
            input_tokens (int): The number of input tokens.
            output_tokens (int): The number of output tokens.

        Returns:
            float: The cost of the completion.
        """
        cost = (
            input_tokens * self.pricing[self.model]["input_tokens"]
            + output_tokens * self.pricing[self.model]["output_tokens"]
        )
        return cost

    def completion(self, prompt: str) -> str:
        """
        Perform a completion task with the given data.
        This method should be overridden by derived classes.
        """
        raise NotImplementedError("Subclasses must override this method.")

    def to_dict(self):
        """
        Convert the completion to a dictionary.
        """
        return {
            "system_role": self.system_role,
            "model": self.model,
            "parameters": self.parameters,
            "cost": self.cost,
            "is_json": self.is_json,
            "test_path": self.test_path,
            "response_message": self.response_message,
            "latency": self.latency,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a completion from a dictionary.
        """
        completion = cls(
            system_role=data["system_role"],
            model=data["model"],
            parameters=data["parameters"],
            pricing_file="",  # Placeholder, should be set correctly in subclasses
        )
        completion.cost = data["cost"]
        completion.is_json = data["is_json"]
        completion.test_path = data["test_path"]
        completion.response_message = data["response_message"]
        completion.latency = data["latency"]
        return completion
