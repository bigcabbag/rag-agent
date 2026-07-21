# 开发用：启动前端 Vite
Set-Location $PSScriptRoot\..\frontend
Write-Host "Starting frontend at http://127.0.0.1:5173" -ForegroundColor Cyan
Write-Host "Backend:  .\\scripts\\dev.ps1  ->  http://127.0.0.1:8000" -ForegroundColor Yellow
npm run dev
