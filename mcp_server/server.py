from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis do .env
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

app = FastAPI(title="Financial Assistant API")

class EmergencyFundRequest(BaseModel):
    monthly_expenses: float
    months: int = 6

@app.post("/tools/calculate_emergency_fund")
def calculate_emergency_fund(data: EmergencyFundRequest):
    try:
        result = data.monthly_expenses * data.months
        logging.info(f"[TOOL] Reserva: {data.monthly_expenses} x {data.months} = {result}")
        return {"result": result}
    except Exception as e:
        logging.error(f"Erro ao calcular reserva: {e}")
        raise HTTPException(status_code=500, detail="Erro no cálculo da reserva")

@app.post("/tools/extract_expense")
def extract_expense(message: dict):
    try:
        user_text = message.get("message", "")
        # lógica simples para extrair número de reais
        import re
        match = re.search(r"(?:r\$\s*)?(\d+[\.,]?\d*)", user_text.lower())
        if match:
            valor = float(match.group(1).replace(",", "."))
            return {"value": valor}
        return {"value": None}
    except Exception as e:
        logging.warning(f"Erro ao extrair despesas: {e}")
        return {"value": None}

@app.get("/tools/get_selic_rate")
def get_selic_rate():
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json"
        response = requests.get(url)
        response.raise_for_status()
        return {"result": float(response.json()[0]['valor'])}
    except Exception as e:
        logging.warning(f"Erro ao obter SELIC: {e}")
        return {"result": -1.0}

@app.get("/tools/get_ipca_rate")
def get_ipca_rate():
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json"
        response = requests.get(url)
        response.raise_for_status()
        return {"result": float(response.json()[0]['valor'])}
    except Exception as e:
        logging.warning(f"Erro ao obter IPCA: {e}")
        return {"result": -1.0}

class InvestmentRequest(BaseModel):
    principal: float
    rate: float
    years: int

@app.post("/tools/simulate_investment")
def simulate_investment(data: InvestmentRequest):
    try:
        result = data.principal * ((1 + data.rate) ** data.years)
        return {"result": result}
    except Exception as e:
        logging.error(f"Erro na simulação de investimento: {e}")
        raise HTTPException(status_code=500, detail="Erro na simulação")

class SavingsCapacityRequest(BaseModel):
    income: float
    expenses: float

@app.post("/tools/analyze_savings_capacity")
def analyze_savings_capacity(data: SavingsCapacityRequest):
    try:
        result = data.income - data.expenses
        return {"result": result}
    except Exception as e:
        logging.error(f"Erro na análise de poupança: {e}")
        raise HTTPException(status_code=500, detail="Erro ao calcular capacidade de poupança")

class SuggestProductsRequest(BaseModel):
    profile: str

@app.post("/tools/suggest_financial_products")
def suggest_financial_products(data: SuggestProductsRequest):
    try:
        produtos = {
            "conservador": ["Tesouro Selic", "CDB grande"],
            "moderado": ["Tesouro IPCA", "LCI"],
            "arrojado": ["Ações", "FII"]
        }
        return {"result": produtos.get(data.profile.lower(), ["Perfil não reconhecido"])}
    except Exception as e:
        logging.error(f"Erro ao sugerir produtos: {e}")
        raise HTTPException(status_code=500, detail="Erro ao sugerir produtos")

@app.get("/tools/ping")
def ping():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor MCP com FastAPI...")
    uvicorn.run("mcp_server.server:app", host="0.0.0.0", port=8000, reload=True)
