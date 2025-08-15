from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
import sys
from pathlib import Path as _P

# 确保 backend 在 sys.path
_ROOT = _P(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
import numpy as np
from tqdm import tqdm

from app.config import get_settings
from app.utils.file_loader import iter_documents
from app.utils.text_splitter import split_text
from app.services.embedding import embed_texts
from app.vectorstore.numpy_store import NumpyStore
from app.vectorstore.faiss_store import FaissStore


def main() -> None:
    load_dotenv()
    s = get_settings()

    print(f"原始文档目录: {s.raw_dir}")
    docs = list(iter_documents(s.raw_dir))
    if not docs:
        print("未在 data/raw 下找到文档，请先放入 FAQ/SOP/政策等文档。")
        return

    chunks: List[Dict] = []
    for d in tqdm(docs, desc="切分文档"):
        parts = split_text(d["text"], s.chunk_size, s.chunk_overlap)
        for p in parts:
            chunks.append({
                "text": p,
                "source": d["source"],
            })

    texts = [c["text"] for c in chunks]
    print(f"共生成片段: {len(texts)}，开始向量化……")
    embeddings = embed_texts(texts)  # (N, dim) 已归一化

    s.index_dir.mkdir(parents=True, exist_ok=True)
    if s.vector_store.lower() == "faiss":
        store = FaissStore(index_dir=s.index_dir, dim=s.embedding_dim)
        store.build(embeddings.astype(np.float32), chunks)
        print(f"FAISS 索引已保存到: {s.index_dir}")
    else:
        store = NumpyStore(index_dir=s.index_dir)
        store.build(embeddings.astype(np.float32), chunks)
        print(f"Numpy 索引已保存到: {s.index_dir}")


if __name__ == "__main__":
    main()


