# 开发用：启动后端 FastAPI（前端请另开终端 npm run dev）
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
Set-Location $PSScriptRoot\..
Write-Host "Starting backend at http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Frontend: cd frontend && npm run dev  ->  http://127.0.0.1:5173" -ForegroundColor Yellow
uv run python main.py
