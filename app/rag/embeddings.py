from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from app.config import get_embedding_model


@lru_cache
def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=get_embedding_model(),
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )