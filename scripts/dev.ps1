# 开发用：自动把 uv 加入 PATH 并启动服务
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
Set-Location $PSScriptRoot\..
uv run python main.py
