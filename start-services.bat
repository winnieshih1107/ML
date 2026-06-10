@echo off
rem Set your Gemini API key here (get it from https://aistudio.google.com/apikey)
set GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE

start "ML Backend" /min cmd /k "set GEMINI_API_KEY=%GEMINI_API_KEY% && cd /d D:\wi\260608\ml-top10\backend && .\venv\Scripts\uvicorn.exe main:app --port 8000"
timeout /t 3 /nobreak >nul
start "ML Frontend" /min cmd /k "cd /d D:\wi\260608\ml-top10\frontend && npm run dev"
