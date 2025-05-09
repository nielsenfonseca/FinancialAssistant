# emergency_fund_agent.py
from .base_agent import BaseAgent
import requests
import os
from langchain_core.messages import SystemMessage, HumanMessage

class EmergencyFundAgent(BaseAgent):
    def __init__(self):
        super().__init__("EmergencyFundAgent")

    def process(self, input_text, state) -> str:
        if "despesas" not in state or not state["despesas"]:
            try:
                response = requests.post(
                    f"{os.getenv('MCP_SERVER_URL')}/tools/extract_expense",
                    json={"message": input_text},
                    timeout=5
                )
                data = response.json()
                if data.get("value"):
                    state["despesas"] = data["value"]
                    state["intencao_pendente"] = False
                    state.pop("pendente_emergency_fund", None)
                else:
                    state["intencao_pendente"] = True
                    state["pendente_emergency_fund"] = True
                    return (
                        "Para calcular sua reserva de emergência, preciso saber o valor médio das suas despesas mensais. "
                        "Você pode me informar isso?"
                    )
            except Exception as e:
                state["intencao_pendente"] = False
                return f"Erro ao tentar entender suas despesas: {e}"

        try:
            response = requests.post(
                f"{os.getenv('MCP_SERVER_URL')}/tools/calculate_emergency_fund",
                json={"monthly_expenses": state["despesas"], "months": 6},
                timeout=5
            )
            valor = response.json().get("result", 0)
            state["intencao_pendente"] = False
            mensagens = [
                SystemMessage(content="Você é um assistente financeiro. Explique o valor de reserva de emergência de forma empática e clara."),
                HumanMessage(content=f"O valor recomendado é R$ {valor:.2f}. Como posso explicar isso ao usuário?")
            ]
            resposta = self.llm(mensagens)
            return getattr(resposta, "content", str(resposta))
        except Exception as e:
            state["intencao_pendente"] = False
            return f"Erro ao consultar ferramenta de cálculo: {e}"