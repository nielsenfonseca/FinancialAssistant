# investment_agent.py
from .base_agent import BaseAgent
import requests
import os
from langchain_core.messages import SystemMessage, HumanMessage

class InvestmentAgent(BaseAgent):
    def __init__(self):
        super().__init__("InvestmentAgent")

    def process(self, input_text, state) -> str:
        try:
            response = requests.post(
                f"{os.getenv('MCP_SERVER_URL')}/tools/investment_advice",
                json={"message": input_text},
                timeout=5
            )
            dica = response.json().get("advice", "Não foi possível obter uma sugestão.")
            mensagens = [
                SystemMessage(content="Você é um assistente financeiro. Explique e contextualize uma sugestão de investimento de forma acessível."),
                HumanMessage(content=f"Sugestão da ferramenta: {dica}")
            ]
            resposta = self.llm(mensagens)
            return getattr(resposta, "content", str(resposta))
        except Exception as e:
            return f"Erro ao consultar sugestão de investimento: {e}"