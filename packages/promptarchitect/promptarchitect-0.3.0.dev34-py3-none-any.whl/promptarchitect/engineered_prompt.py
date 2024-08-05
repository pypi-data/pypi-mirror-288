import json
import logging
import os

import coloredlogs

from promptarchitect.claude_completion import ClaudeCompletion
from promptarchitect.completions.calculated import (
    CalculatedCompletion,
)
from promptarchitect.completions.core import Completion
from promptarchitect.completions.format import FormatCheckCompletion
from promptarchitect.log_error import LogError, Severity
from promptarchitect.openai_completion import OpenAICompletion
from promptarchitect.prompt_file import PromptFile

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
coloredlogs.install(level="INFO")


class EngineeredPrompt(Completion):
    def __init__(self, prompt_file_path: str, output_path: str = "text") -> None:
        super().__init__()

        self._prompt = ""

        self.prompt_file_path = prompt_file_path
        self.output_path = output_path

        self.input_text = ""
        self.errors = LogError()  # Initialize an empty list to store error messages
        self.completion = None  # Declare the completion object

        self.prompt_file = PromptFile(prompt_file_path)
        self.setup_completion()  # Setup completion object

    def setup_completion(self):
        provider = self.prompt_file.metadata.get("provider", "openai")

        try:
            system_role_file = self.prompt_file.metadata.get("system_role", "")
            if system_role_file:
                with open(system_role_file, "r") as file:
                    system_role = file.read()
            else:
                system_role = "You are a helpful assistant."

            if provider.lower() == "openai":
                self.completion = OpenAICompletion(
                    system_role=system_role,
                    model=self.prompt_file.metadata["model"],
                    parameters=self.prompt_file.metadata,
                )
            elif provider.lower() == "anthropic":
                self.completion = ClaudeCompletion(
                    system_role=system_role,
                    model=self.prompt_file.metadata["model"],
                    parameters=self.prompt_file.metadata,
                )
            else:
                raise ValueError(f"Provider {provider} not supported.")

            # TODO: Move this to the specific completion classes
            # if "model" not in self.prompt_file.metadata:
            #     self.errors.log_error(
            #         name=self.prompt_file.filename,
            #         message="No model specified. Using default model.",
            #         severity=Severity.WARNING,
            #     )
            #     self.prompt_file.metadata["model"] = (
            #         DEFAULT_MODEL  # Use default if none specified
            #     )

            os.makedirs(self.output_path, exist_ok=True)
        except Exception as e:
            self.errors.log_error(
                name=self.prompt_file.filename,
                message=f"Error initializing completion: {e}",
                severity=Severity.ERROR,
            )

    def store_to_cache(self):
        cache_file = os.path.join(
            self.output_path, f"{self.prompt_file.metadata['output']}.json"
        )
        with open(cache_file, "w") as file:
            json.dump(self.to_dict(), file, indent=4)

    def execute(
        self, input_text: str = None, input_file: str = None, cached: bool = False
    ) -> str:
        """
        Execute the prompt completion for the EngineeredPrompt object.
        Args:
            input_text (str): The input text to complete.
            input_file (str): The path to the input file.
            cached (bool): Whether to load from the cache if it exists.
        Returns:
            str: The completion response message.
        """
        if cached:
            success = self.load_from_cache()
            if success and self.completion and self.completion.response_message:
                return self.completion.response_message

        if not self.completion:
            self.setup_completion()

        # There are multiple ways to provide input text
        # 1. If input_text is provided, use it
        # 2. If input_file is provided, read from the file
        # 3. If none is provided, see if the prompt file has an input file
        # 4. If none is provided, the input text is an empty string

        if input_text is None and input_file is None:
            input_file = self.prompt_file.metadata.get("input", None)
        elif input_text is None and input_file is None:
            input_text = self.prompt_file.metadata.get("input_text", "")
        elif input_text is None and input_file is not None:
            input_text = self.read_from_input_file(input_file)
        else:
            input_text = input_text if input_text else ""

        logger.debug(f"This is the input text: {input_text}")

        logger.info(
            f"Executing completion for {self.prompt_file.filename} with "
            f"input file {input_file}"
        )
        prompt = f"{self.prompt_file.prompt}\n{input_text}"
        response_text = self.completion.completion(prompt=prompt)
        self.input_file = input_file
        self.latency = self.completion.latency
        self.cost = self.completion.cost
        self.store_to_cache()
        self.store_to_text(response_text)
        return response_text

    def read_from_input_file(self, input_file: str) -> str:
        if not input_file:
            return ""
        with open(input_file, "r") as file:
            input_text = file.read()
        return input_text

    def get_output_path(self):
        return os.path.join(self.output_path, self.prompt_file.metadata["output"])

    def store_to_text(self, response_text: str):
        output_path = os.path.join(
            self.output_path, self.prompt_file.metadata["output"]
        )
        # Check if the output is a json file
        # First check if the response format is specified in the metadata
        if (
            "response_format" in self.prompt_file.metadata
            and "json" in self.prompt_file.metadata["response_format"]
        ):
            with open(output_path, "w") as file:
                json.dump(self.completion.response_message, file, indent=4)
        else:
            with open(output_path, "w") as file:
                file.write(self.completion.response_message)

        return output_path

    def load_from_cache(self) -> bool:
        """Load the completion from a cache file if it exists."""
        cache_file = os.path.join(
            self.output_path, f"{self.prompt_file.metadata['output']}.json"
        )
        # Check if the cache file exists and has data
        if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
            with open(cache_file, "r") as file:
                data = json.load(file)
                self.update_from_dict(data)
                logger.info(f"Loaded completion from cache: {cache_file}")
                return True
        return False

    def update_from_dict(self, data):
        """Update current instance with data from a dictionary."""
        self.input_file = data.get("input_file", self.input_file)
        self.input_text = data.get("input_text", self.input_text)
        self.latency = data.get("latency", self.latency)
        self.cost = data.get("cost", self.cost)
        self.errors = LogError.from_dict(data["errors"])

        # Determine the type of completion object and instantiate it
        completion_type = data.get("completion_type", "OpenAICompletion")
        if completion_type == "CalculatedCompletion":
            if "completion" in data:
                self.completion = CalculatedCompletion.from_dict(data["completion"])
        elif "completion" in data:
            self.completion = OpenAICompletion.from_dict(data["completion"])

        # Restore the response message if available
        if self.completion:
            self.completion.response_message = data.get("response_message", "")

    def to_dict(self):
        return {
            "prompt_file_path": self.prompt_file_path,
            "output_path": self.output_path,
            "input_file": self.input_file,
            "input_text": self.input_text,
            "latency": self.latency,
            "cost": self.cost,
            "errors": self.errors.to_dict(),
            "completion": self.completion.to_dict() if self.completion else None,
            "completion_type": (
                self.completion.__class__.__name__ if self.completion else None
            ),
            "response_message": (
                self.completion.response_message if self.completion else ""
            ),
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(data["prompt_file_path"], data["output_path"])
        obj.input_file = data["input_file"]
        obj.input_text = data["input_text"]
        obj.latency = data["latency"]
        obj.cost = data["cost"]
        obj.errors = (
            LogError.from_dict(data["errors"]) if data.get("errors") else LogError()
        )

        completion_type = data.get("completion_type", "OpenAICompletion")
        if completion_type == "CalculatedCompletion":
            obj.completion = CalculatedCompletion.from_dict(data["completion"])
        elif completion_type == "FormatCheckCompletion":
            obj.completion = FormatCheckCompletion.from_dict(data["completion"])
        else:
            obj.completion = OpenAICompletion.from_dict(data["completion"])

        return obj
