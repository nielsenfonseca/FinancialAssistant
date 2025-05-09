from llm.gemini_model import GeminiModel

class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.llm = GeminiModel()

    def process(self, input_text, state) -> str:
        raise NotImplementedError("Cada agente deve implementar seu próprio método process.")
