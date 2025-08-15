from __future__ import annotations

import threading
from typing import List

import numpy as np
from fastembed import TextEmbedding

from ..config import get_settings


_model_lock = threading.Lock()
_embedder: TextEmbedding | None = None


def _ensure_model() -> TextEmbedding:
    global _embedder
    if _embedder is None:
        with _model_lock:
            if _embedder is None:
                settings = get_settings()
                _embedder = TextEmbedding(model_name=settings.embedding_model)
    return _embedder


def _normalize(vectors: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-12
    return vectors / norms


def embed_texts(texts: List[str]) -> np.ndarray:
    model = _ensure_model()
    # fastembed 返回生成器，逐条/批量产生向量
    vectors = []
    for vec in model.embed(texts):
        vectors.append(vec)
    embeddings = np.asarray(vectors, dtype=np.float32)
    return _normalize(embeddings)


def embed_query(text: str) -> np.ndarray:
    return embed_texts([text]).astype(np.float32)[0]


