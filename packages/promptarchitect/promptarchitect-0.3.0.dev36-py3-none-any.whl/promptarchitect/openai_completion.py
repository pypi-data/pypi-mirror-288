import json
import logging
import re
import timeit
from pathlib import Path

import coloredlogs
import dotenv
import openai
from openai import OpenAI
from retry import retry

from promptarchitect.completions.core import Completion

# Configuring logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
coloredlogs.install(level="INFO")
dotenv.load_dotenv()

DEFAULT_MODEL = "gpt-4o"


class OpenAICompletion(Completion):
    """
    A class to interact with OpenAI API to fetch completions for prompts using
    specified models.
    """

    client = OpenAI()  # Instance of the OpenAI class initialized

    def __init__(self, system_role: str = "", model=DEFAULT_MODEL, parameters={}):
        """
        Initialize the OpenAICompletion class with necessary API client and
        model configuration.

        Args:
            system_role (str): The role assigned to the system in the conversation.
            Defaults to an empty string.
            model (str): The model used for the OpenAI API calls.
            Defaults to 'gpt-4-turbo-preview'.
        """

        super().__init__(parameters)

        price_file_path = Path(__file__).parent / "pricing" / "openai.json"

        with open(price_file_path, "r") as pricing_file:
            self.pricing = json.load(pricing_file)

        # Check if the parameters are valid
        if model not in self.pricing.keys():
            raise ValueError(f"Model {model} not supported.")

        self.system_role = system_role
        self.model = model
        self._prompt = ""

        self.parameters = parameters
        self.cost = 0.0
        self.is_json = False
        self.test_path = ""
        self.response_message = ""
        self.latency = 0.0  # Latency of the completion in seconds

    def _calculate_cost(self, response: dict) -> float:
        """
        Calculate the cost of the completion based on the response from the API.

        Args:
            response (dict): The response from the API.

        Returns:
            float: The cost of the completion.
        """

        # Get input and output tokens
        input_tokens = response["usage"].prompt_tokens
        output_tokens = response["usage"].completion_tokens

        cost = (
            input_tokens * self.pricing[self.model]["input_tokens"]
            + output_tokens * self.pricing[self.model]["output_tokens"]
        )

        return cost

    @retry(
        (openai.OpenAIError),
        delay=5,
        backoff=2,
        max_delay=40,
    )
    def completion(self, prompt: str) -> str:
        """
        Fetches a completion for a given prompt using specified parameters.

        Args:
            parameters (dict, optional): Additional parameters for the completion
            request. Defaults to None.

        Returns:
            str: The content of the completion.
        """

        self._prompt = prompt

        request = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_role},
                {"role": "user", "content": self._prompt},
            ],
        }

        if "response_format" in self.parameters:
            self.is_json = True
            if self.parameters["response_format"].strip() in ["json", "json_object"]:
                response_format = {"type": "json_object"}
                self.parameters["response_format"] = response_format

        # Add the parameters to the request
        for key, value in self.parameters.items() if self.parameters else {}:
            if key in [
                "temperature",
                "max_tokens",
                "top_p",
                "frequency_penalty",
                "presence_penalty",
                "stop",
            ]:
                if key in ["temperature"]:
                    request[key] = float(value)
                elif key in ["max_tokens", "top_p"]:
                    request[key] = int(value)
                else:
                    request[key] = value

        try:
            # Calculate the latency of the completion
            start = timeit.default_timer()
            response = self.client.chat.completions.create(**request)
            end = timeit.default_timer()
            self.latency = end - start
        except openai.BadRequestError as e:
            raise ValueError(f"Bad Request Error (wrong parameters): {e}")

        self._response = dict(response)
        # Calculate the cost of the completion
        self.cost = self._calculate_cost(self._response)

        self.response_message = response.choices[0].message.content
        if self.is_json:
            # OpenAI has the quirks of returning JSON in a weird format
            # With starting and ending quotes. So we need to extract the JSON
            self.response_message = self._extract_json(self.response_message)

        return self.response_message.strip()

    def _extract_json(self, text):
        # Regular expression pattern to find text that looks like JSON
        # This pattern assumes JSON starts with '[' or '{' and ends with ']' or '}'
        pattern = r"\{[\s\S]*\}|\[[\s\S]*\]"

        # Searching the text for JSON pattern
        match = re.search(pattern, text)

        if match:
            json_text = match.group(0)
            try:
                # Validating and returning the JSON object
                _ = json.loads(json_text)
                return json_text
            except json.JSONDecodeError:
                return "The extracted text is not valid JSON."
        else:
            return "No JSON found in the text."

    def to_dict(self):
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
        obj = cls(
            system_role=data["system_role"],
            model=data["model"],
            parameters=data["parameters"],
        )
        obj.cost = data.get("cost", 0.0)
        obj.is_json = data.get("is_json", False)
        obj.test_path = data.get("test_path", "")
        obj.response_message = data.get("response_message", "")
        obj.latency = data.get("latency", 0.0)
        return obj
