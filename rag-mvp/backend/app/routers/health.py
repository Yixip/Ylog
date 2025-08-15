from __future__ import annotations

from fastapi import APIRouter

from ..services.retriever import docs_count
from ..config import get_settings


router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health():
    s = get_settings()
    return {
        "status": "ok",
        "vector_store": s.vector_store,
        "docs": docs_count(),
    }


