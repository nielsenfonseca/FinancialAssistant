import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END, START

from agents.emergency_fund_agent import EmergencyFundAgent
from agents.investment_agent import InvestmentAgent
from agents.generic_agent import GenericAgent
from agents.savings_agent import SavingsAgent

from llm.gemini_model import GeminiModel

# Carrega variáveis de ambiente
load_dotenv()

# Inicializa o LLM
llm = GeminiModel()

# Registra os agentes
agents = {
    "emergency_fund": EmergencyFundAgent(),
    "investment": InvestmentAgent(),
    "generic": GenericAgent(),
    "savings": SavingsAgent(),
}

# 🔁 Roteador com suporte a intenção pendente
def decide_next_node(state):
    print(f"\n🧭 [Roteador] Mensagens no estado: {state.get('messages')}")

    # Se ainda estamos num fluxo em aberto, mantém o agente ativo
    if state.get("intencao_pendente") and state.get("agente_ativo"):
        print(f"↪️ Intenção pendente. Mantendo agente: {state['agente_ativo']}")
        return state["agente_ativo"]

    messages = state.get("messages", [])
    if not messages:
        return "generic"

    entrada = messages[-1].content.lower()

    if state.get("pendente_emergency_fund"):
        return "emergency_fund"

    resposta = llm([
        SystemMessage(content="""
Você é um roteador de agentes financeiros. Seu papel é decidir apenas qual agente deve processar a mensagem do usuário.

Retorne **exatamente um** dos seguintes nomes (somente o nome, nada mais):

- emergency_fund
- investment
- savings
- generic
"""),
        HumanMessage(content=entrada)
    ])

    decisao = getattr(resposta, "content", str(resposta)).strip().lower()
    print(f"🧠 Decisão bruta do LLM: {decisao}")
    decisao = decisao.split()[0]
    validos = {"emergency_fund", "investment", "savings", "generic"}

    if decisao in validos:
        state["agente_ativo"] = decisao
        return decisao

    return "generic"

# Executor de cada agente
def build_agent_node(agent_name):
    print(f"🔧 Registrando agente: {agent_name}")
    agent = agents[agent_name]

    def inner(state):
        messages = state.get("messages", [])
        if not messages:
            print(f"⚠️ Agente '{agent_name}': sem mensagens.")
            return state

        entrada = messages[-1].content
        print(f"🚀 [{agent_name}] Entrada: {entrada}")
        resposta = agent.process(entrada, state)
        messages.append(AIMessage(content=resposta))

        if state.get("intencao_pendente"):
            print("⏳ Intenção pendente continua.")
            return {
                "messages": messages,
                "agente_ativo": agent_name,
                "intencao_pendente": True,
            }
        else:
            print("✅ Fluxo encerrado. Liberando roteador.")
            return {"messages": messages}

    return inner

# Monta o grafo
builder = StateGraph(dict)

# Adiciona o nó de roteamento
builder.add_node("router", lambda state: state)
builder.set_entry_point("router")  # ✅ isso já conecta START → router automaticamente

# Adiciona os agentes
for nome_agente in agents:
    builder.add_node(nome_agente, build_agent_node(nome_agente))
    builder.add_edge(nome_agente, END)

# Conexões condicionais a partir do router
builder.add_conditional_edges("router", decide_next_node)

# Compila
graph = builder.compile()

# Visualiza
print("\n📄 Visualização do grafo em ASCII:")
print(graph.get_graph().draw_ascii())

# Execução do assistente
def main():
    print("🤖 Assistente financeiro iniciado. Digite 'sair' para encerrar.")
    messages = []
    state = {"messages": messages}

    while True:
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            break

        state["messages"].append(HumanMessage(content=user_input))
        result = graph.invoke(state, config={"thread_id": "default"})

        if result and isinstance(result, dict):
            state.update(result)
        else:
            print("⚠️ Resultado inválido.")
            continue

        resposta = state["messages"][-1].content if state["messages"] else "Sem resposta."
        print(f"Assistente: {resposta}\n")

if __name__ == "__main__":
    main()
