from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import chat as chat_router
from .routers import health as health_router
from .services import retriever
from .vectorstore.faiss_store import FaissStore
from .vectorstore.numpy_store import NumpyStore


def create_app() -> FastAPI:
    load_dotenv()  # 读取 .env
    app = FastAPI(title="RAG FAQ Backend", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(chat_router.router)
    app.include_router(health_router.router)

    @app.on_event("startup")
    def _startup() -> None:
        s = get_settings()
        # 选择并加载向量库
        if s.vector_store.lower() == "faiss":
            store = FaissStore(index_dir=s.index_dir, dim=s.embedding_dim)
            try:
                store.load()
            except Exception:
                # 索引可能还未构建
                pass
            retriever.set_vector_store(store)
        else:
            store = NumpyStore(index_dir=s.index_dir)
            try:
                store.load()
            except Exception:
                pass
            retriever.set_vector_store(store)

    return app


app = create_app()


