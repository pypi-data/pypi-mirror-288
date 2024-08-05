import pytest  # noqa: F401
from promptarchitect.completions.core import Completion


def test_completion_initialization():
    completion = Completion()
    assert completion._prompt == ""
    assert completion.cost == 0.0
    assert completion.is_json is False
    assert completion.response_message == ""
    assert completion.parameters == {}
    assert completion.system_role == ""
    assert completion.input_file == ""
    assert completion.latency == 0.0


def test_completion_to_dict():
    completion = Completion()
    completion._prompt = "This is a prompt"
    completion.cost = 1.99
    completion.is_json = True
    completion.response_message = "Completed successfully"
    completion.latency = 0.5
    completion.input_file = "input.txt"

    expected_dict = {
        "prompt": "This is a prompt",
        "cost": 1.99,
        "is_json": True,
        "response_message": "Completed successfully",
        "latency": 0.5,
        "input_file": "input.txt",
    }

    assert completion.to_dict() == expected_dict


def test_completion_from_dict():
    completion_dict = {
        "prompt": "This is a prompt",
        "cost": 1.99,
        "is_json": True,
        "response_message": "Completed successfully",
        "latency": 0.5,
        "input_file": "input.txt",
    }

    completion = Completion.from_dict(completion_dict)

    assert completion._prompt == "This is a prompt"
    assert completion.cost == 1.99  # noqa: PLR2004
    assert completion.is_json is True
    assert completion.response_message == "Completed successfully"
    assert completion.latency == 0.5  # noqa: PLR2004
    assert completion.input_file == "input.txt"
