# generic_agent.py
from .base_agent import BaseAgent
from langchain_core.messages import SystemMessage, HumanMessage

class GenericAgent(BaseAgent):
    def __init__(self):
        super().__init__("GenericAgent")

    def process(self, input_text, state) -> str:
        mensagens = [
            SystemMessage(content="Você é um assistente financeiro gentil e atencioso. Responda de forma clara e útil."),
            HumanMessage(content=input_text)
        ]
        resposta = self.llm(mensagens)
        return getattr(resposta, "content", str(resposta))