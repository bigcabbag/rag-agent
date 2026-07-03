from langchain_core.documents import Document

from app.rag.store import get_vector_store

DEFAULT_TOP_K = 3


def retrieve(query: str, top_k: int = DEFAULT_TOP_K) -> list[Document]:
    """按语义相似度从 Chroma 检索最相关的文档块。"""
    store = get_vector_store()
    if store._collection.count() == 0:
        return []
    return store.similarity_search(query, k=top_k)
