# savings_agent.py
from .base_agent import BaseAgent
import requests
import os
from langchain_core.messages import SystemMessage, HumanMessage

class SavingsAgent(BaseAgent):
    def __init__(self):
        super().__init__("SavingsAgent")

    def process(self, input_text, state) -> str:
        renda = state.get("renda", 5000)
        despesas = state.get("despesas", 3000)
        try:
            response = requests.post(
                f"{os.getenv('MCP_SERVER_URL')}/tools/analyze_savings_capacity",
                json={"income": renda, "expenses": despesas},
                timeout=5
            )
            sobra = response.json().get("result", 0)
            mensagens = [
                SystemMessage(content="Você é um assistente financeiro. Explique com empatia a capacidade de poupança mensal."),
                HumanMessage(content=f"Com uma renda de R$ {renda} e despesas de R$ {despesas}, o usuário pode poupar R$ {sobra:.2f} por mês.")
            ]
            resposta = self.llm(mensagens)
            return getattr(resposta, "content", str(resposta))
        except Exception as e:
            return f"Erro ao calcular capacidade de poupança: {e}"