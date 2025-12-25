from ..utils.llm_client import LLMClient

class BaseAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.llm = LLMClient()

    def process(self, *args, **kwargs):
        """
        Main processing method to be overridden by subclasses.
        """
        raise NotImplementedError
