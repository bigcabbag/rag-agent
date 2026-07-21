# rag-agent

DevKit 研发团队文档助手 — 企业知识库 RAG 学习项目（Python 3.12 + uv + FastAPI + React）。

## 环境要求

- uv（`%USERPROFILE%\.local\bin`）
- Python 3.12（`.python-version`）
- Node.js 18+（M3 前端）

## 快速开始（全栈）

**1. 配置 API Key**

```powershell
copy .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY
```

**2. 启动后端（终端 1）**

```powershell
cd E:\01_Dev\langChain
.\scripts\dev.ps1
```

**3. 启动前端（终端 2）**

```powershell
cd E:\01_Dev\langChain
.\scripts\dev-frontend.ps1
```

**4. 浏览器验收**

打开 http://127.0.0.1:5173

1. 左侧上传 PDF → 看到 `vector_count > 0`
2. 右侧提问（默认流式）→ 逐字生成 + 引用来源
3. 可关「流式输出」对比非流式 `POST /chat`

后端健康检查：http://127.0.0.1:8000/health  
API 文档：http://127.0.0.1:8000/docs

## 仅后端（M0～M2）

```powershell
uv sync
uv run python main.py
```

## 前端环境变量

见 `frontend/.env.example`（默认 `VITE_API_BASE_URL=http://127.0.0.1:8000`）。

## 主要接口

| 接口 | 说明 |
|------|------|
| `POST /documents/upload` | 上传 PDF 入库 |
| `GET /documents/stats` | 向量库统计 |
| `POST /chat` | 非流式对话（JSON 一次返回） |
| `POST /chat/stream` | SSE 流式对话（M3.3+） |

## 学习进度

见 [docs/PLAN.md](./docs/PLAN.md) · 子步 [docs/M3-steps.md](./docs/M3-steps.md) · 面试题 [docs/qa-m3.md](./docs/qa-m3.md)

## Cursor / VS Code

解释器：`.venv\Scripts\python.exe`（`.vscode/settings.json` 已配置）
