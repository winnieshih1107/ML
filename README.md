# 十大機器學習演算法 — 互動學習平台

用 **Streamlit**（雲端一鍵體驗）或 **FastAPI + Next.js**（本地完整版）製作的互動式機器學習學習平台。
涵蓋十大演算法的總覽卡片、比較表、學習順序、互動 Playground、學習指引、程式片段與小測驗。

## 🚀 Live Demo

| 版本 | 網址 | 說明 |
|------|------|------|
| ☁️ Streamlit Cloud | **[https://wi0608.streamlit.app](https://wi0608.streamlit.app)** | 免安裝，直接體驗 |
| 💻 本地完整版 | `http://localhost:3000` | Next.js + FastAPI，見下方說明 |

## ✨ 功能特色

- **十大演算法總覽** — 卡片網格、比較總覽表、初學者建議學習順序
- **互動 Playground** — 即時調整參數，視覺化決策邊界與模型評估指標
- **學習指引** — 核心概念、運作原理、優缺點、應用場景
- **程式片段** — scikit-learn / PyTorch 範例程式碼
- **小測驗** — 每個演算法 3 題，即時批改

## 📁 專案結構

```
ML/
├── streamlit_app.py         ☁️  Streamlit 版（單檔，部署到 Streamlit Cloud）
├── requirements.txt             Streamlit Cloud 依賴
├── start.ps1                    一鍵啟動本地前後端（Windows PowerShell）
├── backend/                 🐍  FastAPI 後端
│   ├── main.py                  API 路由
│   ├── data.py                  十大演算法資料
│   ├── playground.py            互動 Playground 邏輯
│   └── requirements.txt
└── frontend/                ⚛️  Next.js 前端 (App Router + Tailwind CSS)
    ├── app/
    │   ├── page.jsx             首頁（總覽 + 比較表 + 學習順序）
    │   └── algorithm/[id]/page.jsx  演算法詳細頁
    ├── components/              Sidebar / Header / AlgorithmCard / PlaygroundTab…
    ├── lib/api.js               呼叫後端 API
    └── .env.local               設定後端網址（需自行建立，見下方）
```

## ☁️ Streamlit 版（免安裝）

直接開啟 👉 **[https://wi0608.streamlit.app](https://wi0608.streamlit.app)**

不需要安裝任何套件，瀏覽器即可使用全部功能。

### 本地執行 Streamlit

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 💻 本地完整版（FastAPI + Next.js）

### 需求環境

- Python 3.9+
- Node.js 18.17+

### 一鍵啟動（Windows）

```powershell
.\start.ps1
```

開啟 http://localhost:3000（前端）與 http://localhost:8000/docs（API 文件）。

### 手動啟動（需兩個終端機）

**終端機 1 — 後端 FastAPI（埠 8000）**

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

**終端機 2 — 前端 Next.js（埠 3000）**

```bash
cd frontend
npm install
npm run dev
```

**建立 `.env.local`（首次使用需手動建立）**

```
frontend/.env.local
```
內容：
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

## 🔌 API 端點（FastAPI）

| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/api/algorithms` | 十大演算法總覽卡片清單 |
| GET | `/api/algorithms/{id}` | 單一演算法完整詳細（1–10） |
| GET | `/api/algorithms/{id}/playground` | Playground 執行結果 |
| GET | `/api/comparison` | 比較總覽表 |
| GET | `/api/learning-path` | 初學者建議學習順序 |
| GET | `/docs` | FastAPI 自動產生的 API 文件 |
