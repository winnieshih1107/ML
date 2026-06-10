# -*- coding: utf-8 -*-
"""十大機器學習演算法 — FastAPI 後端。

提供前端(Next.js)所需的 JSON API:
  GET /api/algorithms              -> 總覽卡片清單
  GET /api/algorithms/{id}         -> 單一演算法的完整詳細
  GET /api/comparison              -> 比較總覽表
  GET /api/learning-path           -> 初學者建議學習順序
  GET /api/health                  -> 健康檢查

啟動方式:
  uvicorn main:app --reload --port 8000
"""

import os
import time

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai as google_genai

import data
import playground as pg

app = FastAPI(
    title="十大機器學習演算法 API",
    description="提供十大機器學習演算法的總覽、詳細、比較與學習路徑資料。",
    version="1.0.0",
)

# 開發環境允許所有來源（前端可能跑在 3000、5000 等任意埠）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/algorithms")
def get_algorithms():
    """回傳總覽卡片所需的精簡資料清單。"""
    return data.list_cards()


@app.get("/api/algorithms/{algo_id}")
def get_algorithm(algo_id: int):
    """回傳單一演算法的完整詳細資料。"""
    detail = data.get_detail(algo_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="找不到指定的演算法")
    return detail


@app.get("/api/comparison")
def get_comparison():
    """回傳演算法比較總覽表。"""
    return data.comparison_table()


@app.get("/api/learning-path")
def get_learning_path():
    """回傳初學者建議學習順序。"""
    return data.learning_path()


@app.get("/api/algorithms/{algo_id}/quiz")
def get_quiz(algo_id: int):
    """回傳單一演算法的測驗題目。"""
    questions = data.get_quiz(algo_id)
    if questions is None:
        raise HTTPException(status_code=404, detail="找不到題目")
    return questions


@app.get("/api/algorithms/{algo_id}/params")
def get_params(algo_id: int):
    """回傳演算法的 Playground 參數定義。"""
    defs = pg.get_param_defs(algo_id)
    if not defs:
        raise HTTPException(status_code=404, detail="找不到參數定義")
    return defs


_CHAT_SYSTEM = """你是「十大機器學習演算法」學習平台的 AI 助教。本平台涵蓋以下十種演算法：
線性迴歸、邏輯迴歸、決策樹、隨機森林、支援向量機 (SVM)、K-近鄰演算法 (KNN)、K-Means 分群、主成分分析 (PCA)、梯度提升 (Gradient Boosting / XGBoost)、神經網路。

你的職責：
- 用繁體中文回答機器學習相關問題，解釋原理、優缺點與使用場景。
- 回答簡潔清晰，適合初學者至中階學習者。
- 若問題與機器學習無關，請友善地引導回 ML 主題。"""


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


@app.post("/api/chat")
def chat(body: ChatRequest):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY 未設定，請在後端設定環境變數。")

    client = google_genai.Client(api_key=api_key)
    messages = body.messages
    contents = [
        {"role": "user" if m.role == "user" else "model",
         "parts": [{"text": m.content}]}
        for m in messages
    ]
    for model in ["gemini-2.5-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash"]:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config={"system_instruction": _CHAT_SYSTEM},
                )
                return {"reply": response.text}
            except Exception as e:
                err = str(e)
                if "503" in err or "UNAVAILABLE" in err or "429" in err:
                    time.sleep(2)
                    continue
                raise HTTPException(status_code=502, detail=err)
    raise HTTPException(status_code=503, detail="AI 服務暫時繁忙，請稍後再試。")


class PlaygroundRequest(BaseModel):
    params: dict = {}


@app.post("/api/algorithms/{algo_id}/playground")
def run_playground(algo_id: int, body: PlaygroundRequest):
    """執行 Playground 模擬，回傳資料點、決策邊界與評估指標。"""
    result = pg.run(algo_id, body.params)
    if result is None:
        raise HTTPException(status_code=404, detail="找不到演算法")
    return result


@app.get("/")
def root():
    return {
        "message": "十大機器學習演算法 API",
        "docs": "/docs",
        "endpoints": [
            "/api/algorithms",
            "/api/algorithms/{id}",
            "/api/comparison",
            "/api/learning-path",
        ],
    }
