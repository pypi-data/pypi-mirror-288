from promptarchitect.openai_completion import DEFAULT_MODEL, OpenAICompletion


def test_completion():
    completion = OpenAICompletion("You're a friendly assistant.")
    prompt = "What is the capital of France?"

    response = completion.completion(prompt)

    assert response is not None


def test_assign_parameters():
    parameters = {"temperature": 0.7}
    completion = OpenAICompletion("You're a friendly assistant.", parameters=parameters)

    assert completion.parameters == parameters
    assert completion.model == DEFAULT_MODEL
