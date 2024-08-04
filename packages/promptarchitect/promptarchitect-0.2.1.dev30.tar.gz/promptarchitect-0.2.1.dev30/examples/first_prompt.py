from pathlib import Path

from promptarchitect import EngineeredPrompt

prompt_path = Path(__file__).parent / "prompts" / "podcast_titels.prompt"
input_file_path = (
    Path(__file__).parent / "inputs" / "podcast_titels" / "beschrijving.txt"
)

# Initialize the EngineeredPrompt
prompt = EngineeredPrompt(
    prompt_file_path=str(prompt_path), output_path="output_directory"
)

# Execute the prompt
response = prompt.execute(input_file=str(input_file_path), cached=False)

print(response)

# Use a cached response
response = prompt.execute(input_file=str(input_file_path), cached=True)

print(response)

# Change the input for the prompt
response2 = prompt.execute(
    input_text="De podcast gaat over ethiek en de invloed op de maatschappij van AI."
)

print(response2)
