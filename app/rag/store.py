from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.rag.embeddings import get_embeddings

CHROMA_DIR = Path("data/chroma")
COLLECTION_NAME = "rag_documents"


def get_vector_store() -> Chroma:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )


def index_chunks(chunks: list[Document], source: str) -> int:
    """把切块写入 Chroma；同名文件会先删旧向量再写入。"""
    for chunk in chunks:
        chunk.metadata["source"] = source

    store = get_vector_store()
    existing = store.get(where={"source": source})
    if existing["ids"]:
        store.delete(ids=existing["ids"])

    store.add_documents(chunks)
    return len(chunks)


def get_index_stats() -> dict[str, str | int]:
    store = get_vector_store()
    return {
        "collection": COLLECTION_NAME,
        "vector_count": int(store._collection.count()),
    }
