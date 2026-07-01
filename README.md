# rag-agent

企业知识库 RAG 学习项目（Python 3.12 + uv + FastAPI）。

## 环境要求

- uv（已安装到 `%USERPROFILE%\.local\bin`）
- Python 3.12（由 uv 管理，见 `.python-version`）

## 快速开始

```powershell
# 若终端找不到 uv，先执行：
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"

cd E:\langChain
uv sync
uv run python main.py
```

浏览器打开 http://127.0.0.1:8000/health 应返回 `{"status":"ok",...}`

**对话接口** `POST /chat`：

```json
{ "message": "你好", "system_prompt": "可选，设定 AI 角色" }
```

API 文档：http://127.0.0.1:8000/docs

## API Key（稍后配置）

1. `copy .env.example .env`
2. 填入 DeepSeek 或通义 API Key
3. 下一节协作 session 接入 LangChain

## Cursor / VS Code

打开本文件夹后，选择解释器：`.venv\Scripts\python.exe`（`.vscode/settings.json` 已配置）
