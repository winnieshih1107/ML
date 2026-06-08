# 啟動後端 (FastAPI) + 前端 (Next.js)
Write-Host "啟動後端 FastAPI (port 8000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PSScriptRoot\backend'; python -m uvicorn main:app --reload --port 8000"

Start-Sleep -Seconds 2

Write-Host "啟動前端 Next.js (port 3000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "前端: http://localhost:3000" -ForegroundColor Green
Write-Host "後端 API 文件: http://localhost:8000/docs" -ForegroundColor Green
