class Completion:
    """
    Abstract base class for completions.
    """

    def __init__(self, parameters={}):
        self._prompt = ""
        self.cost = 0.0
        self.is_json = False
        self.response_message = ""
        self.parameters = parameters
        self.system_role = ""
        self.input_file = ""
        self.latency = 0.0  # Latency of the completion in seconds

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
            "prompt": self._prompt,
            "cost": self.cost,
            "is_json": self.is_json,
            "response_message": self.response_message,
            "latency": self.latency,
            "input_file": self.input_file,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a completion from a dictionary.
        """
        completion = cls()
        completion._prompt = data["prompt"]
        completion.cost = data["cost"]
        completion.is_json = data["is_json"]
        completion.response_message = data["response_message"]
        completion.latency = data["latency"]
        completion.input_file = data["input_file"] if "input_file" in data else ""
        return completion
