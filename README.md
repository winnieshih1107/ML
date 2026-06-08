# 十大機器學習演算法 — 互動網頁

用 **FastAPI(後端)+ Next.js + Tailwind CSS(前端)** 製作的互動式學習網頁。
使用者可依十大主題瀏覽:左側目錄導覽、總覽卡片網格、比較總覽表、建議學習順序,
點擊任一演算法可進入動態詳細頁(核心概念、運作原理、優缺點、應用場景、程式片段)。

## 專案結構

```
ml-top10/
├── backend/                 FastAPI 後端
│   ├── main.py              API 入口與路由
│   ├── data.py              十大演算法資料
│   └── requirements.txt
└── frontend/                Next.js 前端 (App Router + Tailwind)
    ├── app/
    │   ├── page.jsx                 首頁(總覽 + 比較表 + 學習順序)
    │   ├── algorithm/[id]/page.jsx  單一演算法動態詳細頁
    │   ├── layout.jsx / globals.css / not-found.jsx
    ├── components/          Sidebar / Header / AlgorithmCard / ComparisonTable / AlgoIcon
    ├── lib/api.js           呼叫後端 API 的工具
    └── .env.local           設定後端網址
```

## API 端點(FastAPI)

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/algorithms` | 十大演算法總覽卡片清單 |
| GET | `/api/algorithms/{id}` | 單一演算法完整詳細(1~10) |
| GET | `/api/comparison` | 比較總覽表 |
| GET | `/api/learning-path` | 初學者建議學習順序 |
| GET | `/docs` | FastAPI 自動產生的 API 文件 |

## 啟動方式(需開兩個終端機)

### 1. 後端 FastAPI(埠 8000)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

啟動後可開 http://localhost:8000/docs 測試 API。

### 2. 前端 Next.js(埠 3000)

另開一個終端機:

```bash
cd frontend
npm install
npm run dev
```

開啟 http://localhost:3000 即可看到網頁。

> `.env.local` 已設定 `NEXT_PUBLIC_API_BASE=http://localhost:8000`,
> 若後端改用其他埠或網址,修改這個值即可。

## 需求環境

- Python 3.9+
- Node.js 18.17+(Next.js 14 需求)

## 運作說明

前端的首頁與詳細頁皆為 Next.js Server Component,在伺服器端透過 `lib/api.js`
向 FastAPI 抓取資料後渲染。後端已開啟 CORS 允許 `localhost:3000` 存取。
若前端顯示「無法連線到後端 API」,代表 FastAPI 尚未啟動,請先完成步驟 1。
