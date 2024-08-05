import json
import logging
import os
import time

import coloredlogs

from promptarchitect.completions.calculated import (
    CalculatedCompletion,
    Operation,
    Unit,
)
from promptarchitect.completions.format import FormatCheckCompletion
from promptarchitect.engineered_prompt import EngineeredPrompt
from promptarchitect.log_error import LogError, Severity
from promptarchitect.openai_completion import OpenAICompletion

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
coloredlogs.install(level="INFO")


class PromptValidation:
    """
    Run one test prompt for the EngineeredPrompt object.
    """

    def __init__(
        self,
        test_id: str,
        test_prompt: str,
        test_completion_input: str,
        engineered_prompt: EngineeredPrompt,
    ) -> None:
        self.test_id = test_id
        self.test_prompt = test_prompt
        self.test_completion_input = test_completion_input
        self.engineered_prompt = engineered_prompt
        self.passed = False
        self.completion = None
        self.cost = 0.0
        self.duration = 0.0
        self.last_run = None
        self.errors = LogError()  # Initialize an empty list to store error messages

    def apply_test_operation(data, operation: Operation, unit: Unit):
        try:
            if unit == Unit.LINES:
                items = data.split("\n")
            elif unit == Unit.WORDS:
                items = data.split()
            elif unit == Unit.CHARACTERS:
                items = list(data)  # Convert string to list of characters
            else:
                raise ValueError(f"Unsupported unit: {unit}")

            if operation == Operation.MAX:
                return max(items, key=len)
            elif operation == Operation.MIN:
                return min(items, key=len)
            elif operation == Operation.COUNT:
                return len(items)
            else:
                raise ValueError(f"Unsupported operation: {operation}")

        except Exception as e:
            print(f"An error occurred while applying the operation: {str(e)}")
            return None

    def run_test(self, model: str = None) -> dict:
        """
        Run the test prompt for the EngineeredPrompt object.

        Args:
            model (str): Optional overwrite of the model to use for the completion.

        Returns:
            None
        """

        # Execute the test prompt

        # Check if the completion is already run
        stored_data_file = os.path.join(
            self.engineered_prompt.output_path, f"{self.test_id}.json"
        )
        if os.path.exists(stored_data_file):
            try:
                with open(stored_data_file, "r") as f:
                    stored_data = json.load(f)
                pv = PromptValidation.from_dict(stored_data)
                self.completion = pv.completion
                self.last_run = pv.last_run
                self.passed = pv.passed
                self.cost = pv.cost
                self.duration = pv.duration
                self.test_completion_input = pv.test_completion_input
                logger.info(f"Using cached test run from {stored_data_file}")
            except Exception as e:
                self.errors.log_error(
                    name=self.engineered_prompt.prompt_file.filename,
                    message=f"Error reading from cache: {e}. Skipping test",
                    severity=Severity.ERROR,
                )
        else:
            # Define validation parameters to set the temperature low
            # so the completion is more factual
            # Restrict the number of tokens to get a short description
            # if the validation fails
            parameters = {
                "temperature": 0.2,
            }

            oc = None

            # Check if the test prompt is a calculated operation
            # Or is a format check
            calc = CalculatedCompletion()
            format = FormatCheckCompletion()
            if calc.calculated_operations_used(self.test_prompt):
                oc = calc
            elif format.format_check_used(self.test_prompt):
                oc = format
            else:
                # Run the test prompt using the LLM
                oc = OpenAICompletion(
                    system_role="Je bent een prompt tester.",
                    model=(
                        model
                        if model
                        else self.engineered_prompt.prompt_file.metadata["model"]
                    ),
                    parameters=parameters,
                )
            response = oc.completion(
                f"{self.test_prompt}\n{self.test_completion_input}"
            )
            self.test_completion = response
            self.cost = oc.cost
            self.duration = oc.latency
            self.last_run = time.strftime("%Y-%m-%d %H:%M:%S")

            self.completion = oc
            if self.test_completion.startswith("JA") or self.test_completion.startswith(
                "YES"
            ):
                self.passed = True

            stored_data = self.to_dict()
            with open(stored_data_file, "w") as f:
                f.write(json.dumps(stored_data, indent=4))

            return self.passed

    def to_dict(self):
        completion_data = self.completion.to_dict() if self.completion else None
        if self.completion:
            completion_data["completion_type"] = type(self.completion).__name__

        return {
            "test_id": self.test_id,
            "test_prompt": self.test_prompt,
            "test_completion": self.test_completion,
            "passed": self.passed,
            "completion": completion_data,
            "engineered_prompt": self.engineered_prompt.to_dict(),
            "last_run": self.last_run,
            "errors": self.errors.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        obj = cls(
            data["test_id"],
            data["test_prompt"],
            data["test_completion"],
            EngineeredPrompt.from_dict(data["engineered_prompt"]),
        )
        obj.passed = data["passed"]
        obj.last_run = data["last_run"]
        obj.errors = LogError.from_dict(data.get("errors", {}))

        if "completion" in data and data["completion"] is not None:
            completion_type = data["completion"].get(
                "completion_type", "OpenAICompletion"
            )
            if completion_type == "CalculatedCompletion":
                obj.completion = CalculatedCompletion.from_dict(data["completion"])
            elif completion_type == "FormatCheckCompletion":
                obj.completion = FormatCheckCompletion.from_dict(data["completion"])
            else:
                obj.completion = OpenAICompletion.from_dict(data["completion"])

        return obj
