from promptarchitect.claude_completion import DEFAULT_MODEL, ClaudeCompletion


def test_completion():
    completion = ClaudeCompletion("You're a friendly assistant.")
    prompt = "What is the capital of France?"

    response = completion.completion(prompt)

    assert response is not None


def test_assign_parameters():
    parameters = {"temperature": 0.7}
    completion = ClaudeCompletion("You're a friendly assistant.", parameters=parameters)

    assert completion.parameters == parameters
    assert completion.model == DEFAULT_MODEL
