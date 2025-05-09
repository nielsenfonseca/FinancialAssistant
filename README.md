# 💸 FinancialAssistant

O **FinancialAssistant** é um assistente financeiro inteligente que utiliza LLMs (Modelos de Linguagem) e uma arquitetura modular baseada em agentes para ajudar usuários a:

- 📊 Calcular sua **reserva de emergência**
- 💰 Avaliar sua **capacidade de poupança**
- 📈 Obter **sugestões de investimento**
- 🤝 Conversar sobre **educação financeira** em geral

Ele integra ferramentas externas (APIs) para cálculos e simulações financeiras, e usa o LLM para explicar as respostas de forma humana, empática e personalizada.

---

## 🚀 Tecnologias utilizadas

- [Python 3.10+](https://www.python.org/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://www.langchain.com/)
- [Google Gemini (via langchain_google_genai)](https://ai.google.dev/)
- [Requests](https://docs.python-requests.org/)
- [.env + dotenv](https://pypi.org/project/python-dotenv/)

---

## 🧠 Arquitetura

O projeto é composto por:

### 1. **Agentes Especializados** (pasta `agents/`)
Cada agente é responsável por um tipo de assistência:

- `GenericAgent` → inicia conversas gerais e educacionais
- `EmergencyFundAgent` → ajuda a montar uma reserva de emergência
- `SavingsAgent` → analisa sua capacidade de poupar mensalmente
- `InvestmentAgent` → sugere investimentos com base em seu perfil

Todos usam LLMs para **explicar o resultado das ferramentas** de forma clara e empática.

### 2. **Grafo conversacional (LangGraph)**
- Um roteador com LLM detecta a intenção do usuário e direciona para o agente certo
- Cada agente pode manter o controle da conversa por múltiplas mensagens, usando `state["intencao_pendente"]`

### 3. **Ferramentas externas (API)**
APIs externas realizam os cálculos de:
- Gasto médio mensal
- Valor ideal de reserva de emergência
- Capacidade de poupança
- Sugestões de investimento

---

## 🛠 Como rodar o projeto localmente

```bash
# 1. Clone o repositório
$ git clone https://github.com/seu-usuario/FinancialAssistant.git
$ cd FinancialAssistant

# 2. Crie um ambiente virtual
$ python -m venv venv
$ source venv/bin/activate  # ou venv\Scripts\activate no Windows

# 3. Instale as dependências
$ pip install -r requirements.txt

# 4. Configure sua chave .env
GOOGLE_API_KEY=xxxxxx
MCP_SERVER_URL=http://localhost:8000

# 5. Rode o assistente
$ python main.py
```

---

## 📁 Estrutura de arquivos

```
FinancialAssistant/
├── agents/
│   ├── base_agent.py
│   ├── emergency_fund_agent.py
│   ├── generic_agent.py
│   ├── investment_agent.py
│   └── savings_agent.py
├── llm/
│   └── gemini_model.py
├── main.py
├── .env
└── requirements.txt
```

---

## ✨ Exemplo de conversa

```
Você: Quero montar uma reserva de emergência
Assistente: Para calcular sua reserva de emergência, preciso saber o valor médio das suas despesas mensais. Pode me informar?

Você: Gasto cerca de 2000 reais por mês
Assistente: Com base nisso, sua reserva ideal seria de aproximadamente R$ 12.000,00 (6 meses de despesas). Assim você fica protegido em caso de imprevistos. Posso te ajudar a começar esse planejamento se quiser!
```

---

## 🤝 Contribuição
Pull requests são bem-vindos! Para grandes mudanças, abra uma issue primeiro para discutir o que você gostaria de modificar.

---

## 📄 Licença
MIT

---

> Desenvolvido com 💙 por Nielsen com suporte de LLMs para empoderar pessoas financeiramente
