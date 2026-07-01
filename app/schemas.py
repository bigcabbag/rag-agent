from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="用户问题")
    system_prompt: str | None = Field(
        default=None,
        description="可选系统提示词，用来设定 AI 角色",
    )


class ChatResponse(BaseModel):
    reply: str
    model: str


class ChunkPreview(BaseModel):
    index: int
    content: str
    metadata: dict


class UploadResponse(BaseModel):
    filename: str
    chunk_count: int
    chunk_size: int
    chunk_overlap: int
    previews: list[ChunkPreview]
