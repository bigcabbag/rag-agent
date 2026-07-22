"""M4.2：LangGraph CRAG — retrieve → grade → rewrite | generate | abstain."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal, TypedDict

from langchain_core.documents import Document
from langgraph.graph import END, START, StateGraph

from app.llm import chat
from app.rag.context import RAG_SYSTEM_PROMPT, build_context
from app.rag.retriever import retrieve
 
MAX_REWRITES = 1

GRADE_PROMPT = """你是检索质量评估员。判断文档片段是否能帮助回答用户问题。

用户问题：{question}

文档片段：
{docs}

哪些片段与问题相关且可用于回答？只输出相关编号（逗号分隔，如 1,3）。
若全部不相关，只输出 NONE。"""

REWRITE_PROMPT = """用户原问题：{question}

当前检索结果与问题不够相关。请改写为一个更适合在 DevKit 项目文档（PLAN、M3-steps、qa 卡、API 说明）里检索的简短中文问题。
只输出改写后的问题，不要解释。"""

ABSTAIN_EMPTY_KB = "知识库中暂无相关文档，请先上传 PDF 或运行 import_docs.py。"
ABSTAIN_NO_RELEVANT = "文档中未找到相关信息，无法回答该问题。"


class CragState(TypedDict, total=False):
    question: str
    search_query: str
    top_k: int
    system_prompt: str | None
    documents: list[Document]
    relevant_docs: list[Document]
    rewrite_count: int
    route: Literal["generate", "rewrite", "abstain"]
    abstain_reply: str
    rag_prompt: str
    sources: list[dict]


def _format_docs_for_grade(docs: list[Document]) -> str:
    lines: list[str] = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "未知")
        snippet = doc.page_content[:300].replace("\n", " ")
        lines.append(f"[{i}] 来源 {source}\n{snippet}")
    return "\n\n".join(lines)


def _parse_grade_response(raw: str, docs: list[Document]) -> list[Document]:
    text = raw.strip().upper()
    if "NONE" in text or not text:
        return []
    relevant: list[Document] = []
    for i, doc in enumerate(docs, start=1):
        if str(i) in raw:
            relevant.append(doc)
    return relevant


async def _retrieve_node(state: CragState) -> dict:
    docs = retrieve(state["search_query"], top_k=state["top_k"])
    return {"documents": docs}


async def _grade_node(state: CragState) -> dict:
    docs = state.get("documents") or []
    if not docs:
        return {"route": "abstain", "abstain_reply": ABSTAIN_EMPTY_KB}

    raw = await chat(
        GRADE_PROMPT.format(
            question=state["question"],
            docs=_format_docs_for_grade(docs),
        ),
        system_prompt="你是严格的文档相关性评审，只输出编号或 NONE。",
    )
    relevant = _parse_grade_response(raw, docs)
    if relevant:
        return {"relevant_docs": relevant, "route": "generate"}
    if state.get("rewrite_count", 0) < MAX_REWRITES:
        return {"route": "rewrite"}
    return {"route": "abstain", "abstain_reply": ABSTAIN_NO_RELEVANT}


async def _rewrite_node(state: CragState) -> dict:
    new_query = await chat(
        REWRITE_PROMPT.format(question=state["question"]),
        system_prompt="只输出改写后的问题。",
    )
    query = new_query.strip() or state["question"]
    return {
        "search_query": query,
        "rewrite_count": state.get("rewrite_count", 0) + 1,
    }


async def _build_generate_node(state: CragState) -> dict:
    docs = state.get("relevant_docs") or []
    context, sources = build_context(docs)
    rag_prompt = RAG_SYSTEM_PROMPT.format(context=context)
    system_prompt = state.get("system_prompt")
    if system_prompt:
        rag_prompt = f"{system_prompt}\n\n{rag_prompt}"
    return {"rag_prompt": rag_prompt, "sources": sources}


async def _abstain_node(state: CragState) -> dict:
    reply = state.get("abstain_reply") or ABSTAIN_NO_RELEVANT
    return {"abstain_reply": reply, "sources": []}


def _route_after_grade(state: CragState) -> str:
    route = state.get("route", "abstain")
    if route == "generate":
        return "build_generate"
    if route == "rewrite":
        return "rewrite"
    return "abstain"


@lru_cache
def get_crag_graph():
    builder = StateGraph(CragState)
    builder.add_node("retrieve", _retrieve_node)
    builder.add_node("grade", _grade_node)
    builder.add_node("rewrite", _rewrite_node)
    builder.add_node("build_generate", _build_generate_node)
    builder.add_node("abstain", _abstain_node)

    builder.add_edge(START, "retrieve")
    builder.add_edge("retrieve", "grade")
    builder.add_conditional_edges(
        "grade",
        _route_after_grade,
        {
            "build_generate": "build_generate",
            "rewrite": "rewrite",
            "abstain": "abstain",
        },
    )
    builder.add_edge("rewrite", "retrieve")
    builder.add_edge("build_generate", END)
    builder.add_edge("abstain", END)
    return builder.compile()


async def run_crag_prepare(
    message: str,
    *,
    top_k: int = 3,
    system_prompt: str | None = None,
) -> tuple[str | None, list[dict], str | None]:
    """CRAG 预处理：与 prepare_rag_stream 相同返回值。"""
    graph = get_crag_graph()
    result = await graph.ainvoke(
        {
            "question": message,
            "search_query": message,
            "top_k": top_k,
            "system_prompt": system_prompt,
            "rewrite_count": 0,
        }
    )

    if result.get("route") == "abstain" or result.get("abstain_reply"):
        return None, [], result.get("abstain_reply", ABSTAIN_NO_RELEVANT)

    return result.get("rag_prompt"), result.get("sources") or [], None
