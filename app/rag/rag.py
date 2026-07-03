from app.llm import chat
from app.rag.retriever import retrieve

RAG_SYSTEM_PROMPT = """你是一个企业知识库助手。请仅根据以下参考文档回答问题。
如果参考文档中没有相关信息，请明确说「文档中未找到相关信息」，不要编造。

参考文档：
{context}"""


def _build_context(docs: list) -> tuple[str, list[dict]]:
    parts: list[str] = []
    sources: list[dict] = []

    for i, doc in enumerate(docs, start=1):
        source = str(doc.metadata.get("source", "未知"))
        page = doc.metadata.get("page", "?")
        parts.append(f"[{i}] 来源: {source} 第{page}页\n{doc.page_content}")
        sources.append(
            {
                "source": source,
                "page": page,
                "content": doc.page_content[:200],
            }
        )

    return "\n\n".join(parts), sources


async def rag_chat(
    message: str,
    *,
    top_k: int = 3,
    system_prompt: str | None = None,
) -> tuple[str, list[dict]]:
    docs = retrieve(message, top_k=top_k)
    if not docs:
        return "知识库中暂无相关文档，请先上传 PDF。", []

    context, sources = _build_context(docs)
    rag_prompt = RAG_SYSTEM_PROMPT.format(context=context)
    if system_prompt:
        rag_prompt = f"{system_prompt}\n\n{rag_prompt}"

    reply = await chat(message, system_prompt=rag_prompt)
    return reply, sources
