from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from ..config import get_settings
from .embedding import embed_query


_VECTOR_STORE = None  # 运行时注入（numpy/faiss）


def set_vector_store(store) -> None:
    global _VECTOR_STORE
    _VECTOR_STORE = store


def retrieve(question: str, top_k: int = 4) -> List[Dict]:
    assert _VECTOR_STORE is not None, "向量索引未加载，请先运行 ingest.py 并启动应用"
    q = embed_query(question)
    results: List[Tuple[float, Dict]] = _VECTOR_STORE.search(q, top_k)
    contexts: List[Dict] = []
    for score, meta in results:
        contexts.append({
            "text": meta.get("text", ""),
            "source": meta.get("source", ""),
            "score": float(score),
        })
    return contexts


def docs_count() -> int:
    if _VECTOR_STORE is None:
        return 0
    return getattr(_VECTOR_STORE, "docs_count", 0)


