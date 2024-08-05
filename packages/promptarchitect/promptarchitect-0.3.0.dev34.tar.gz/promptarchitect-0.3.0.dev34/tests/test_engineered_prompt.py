import pytest  # noqa: F401
from promptarchitect.engineered_prompt import EngineeredPrompt

# Sample prompt data to use in tests
valid_prompt_content = """
---
key: value
output: output.txt
---
"""


# Define fixtures to use in your tests
@pytest.fixture
def valid_prompt_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "prompt.txt"
    p.write_text(valid_prompt_content)
    return p


def test_execute(valid_prompt_file):
    ep = EngineeredPrompt(prompt_file_path=str(valid_prompt_file))

    # Test with input_text
    response_text = ep.execute(
        input_text="What's the capital The Netherlands.", cached=False
    )

    assert "Amsterdam" in response_text
