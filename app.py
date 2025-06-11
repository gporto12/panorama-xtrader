
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class BacktestRequest(BaseModel):
    ativo: str
    timeframe: str
    data_inicial: str
    data_final: str

@app.post("/rodar_backtest")
def rodar_backtest(req: BacktestRequest):
    df = yf.download(req.ativo, start=req.data_inicial, end=req.data_final, interval=req.timeframe)
    if df.empty:
        return {"erro": "Dados não encontrados para o ativo ou período."}

    df["resultado"] = "win"
    df["lucro"] = 100
    df["rr"] = 2

    total_trades = len(df)
    wins = (df["resultado"] == "win").sum()
    taxa_acerto = wins / total_trades * 100 if total_trades > 0 else 0
    lucro_total = df["lucro"].sum()
    rr_medio = df["rr"].mean()

    return {
        "ativo": req.ativo,
        "timeframe": req.timeframe,
        "total_trades": total_trades,
        "taxa_acerto": round(taxa_acerto, 2),
        "lucro_total": round(lucro_total, 2),
        "rr_medio": round(rr_medio, 2),
    }
