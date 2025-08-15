from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.retriever import retrieve
from ..services.rag import answer_question
from ..config import get_settings


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    question: str
    top_k: int = 4
    session_id: Optional[str] = None


class ContextItem(BaseModel):
    text: str
    source: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    contexts: List[ContextItem]
    latency_ms: int
    model: str


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> Any:
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="question 为空")
    t0 = time.time()
    contexts = retrieve(req.question, req.top_k)
    answer = answer_question(req.question, contexts)
    latency_ms = int((time.time() - t0) * 1000)
    settings = get_settings()
    return ChatResponse(
        answer=answer,
        contexts=[ContextItem(**c) for c in contexts],
        latency_ms=latency_ms,
        model=settings.openai_model if settings.llm_provider == "openai" else settings.ollama_model,
    )


