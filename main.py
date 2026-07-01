from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.config import get_settings
from app.llm import chat
from app.rag.loader import (
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_CHUNK_SIZE,
    load_and_split_pdf,
)
from app.schemas import ChatRequest, ChatResponse, ChunkPreview, UploadResponse

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PREVIEW_CHARS = 200

app = FastAPI(title="RAG Agent", version="0.1.0")


@app.get("/health")
async def health():
    return {"status": "ok", "message": "服务运行中"}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(body: ChatRequest):

    
    try:
        settings = get_settings()
        reply = await chat(body.message, body.system_prompt)
        return ChatResponse(reply=reply, model=settings["model"])
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"调用 DeepSeek 失败: {exc}",
        ) from exc


@app.post("/documents/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """M2.1：上传 PDF，解析并切块（暂不写入向量库）。"""
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="目前只支持 PDF 文件")

    save_path = UPLOAD_DIR / file.filename
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="文件为空")

    save_path.write_bytes(content)

    try:
        chunks = load_and_split_pdf(save_path)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"PDF 解析失败: {exc}",
        ) from exc

    previews = [
        ChunkPreview(
            index=i,
            content=chunk.page_content[:PREVIEW_CHARS],
            metadata=chunk.metadata,
        )
        for i, chunk in enumerate(chunks[:3])
    ]

    return UploadResponse(
        filename=file.filename,
        chunk_count=len(chunks),
        chunk_size=DEFAULT_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CHUNK_OVERLAP,
        previews=previews,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
