from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class Settings(BaseModel):
    # LLM
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2:0.5b")

    dashscope_api_key: str = os.getenv("DASHSCOPE_API_KEY", "")
    dashscope_model: str = os.getenv("DASHSCOPE_MODEL", "qwen-plus")

    # Embedding / Vector store
    vector_store: str = os.getenv("VECTOR_STORE", "numpy")  # numpy 默认更稳妥
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
    embedding_dim: int = int(os.getenv("EMBEDDING_DIM", "384"))
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))

    # Paths
    # 以 backend 目录为基准
    base_dir: Path = Path(__file__).resolve().parents[1]
    data_dir: Path = base_dir / "data"
    index_dir: Path = data_dir / "index"
    chunks_dir: Path = data_dir / "chunks"
    raw_dir: Path = data_dir / "raw"

    # Server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    # 确保目录存在
    _settings.data_dir.mkdir(parents=True, exist_ok=True)
    _settings.index_dir.mkdir(parents=True, exist_ok=True)
    _settings.chunks_dir.mkdir(parents=True, exist_ok=True)
    _settings.raw_dir.mkdir(parents=True, exist_ok=True)
    return _settings


