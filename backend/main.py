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

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import data
import playground as pg

app = FastAPI(
    title="十大機器學習演算法 API",
    description="提供十大機器學習演算法的總覽、詳細、比較與學習路徑資料。",
    version="1.0.0",
)

# 允許 Next.js 前端(預設跑在 3000 埠)跨來源存取
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
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
