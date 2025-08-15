from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

try:
    import faiss  # type: ignore
except Exception:  # pragma: no cover - 可选依赖
    faiss = None  # type: ignore


@dataclass
class FaissStore:
    index_dir: Path
    dim: int

    def __post_init__(self) -> None:
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.index_dir / "faiss.index"
        self.meta_path = self.index_dir / "meta.jsonl"
        self._index = None
        self._metas: List[Dict] = []

    def _require_faiss(self) -> None:
        if faiss is None:
            raise RuntimeError("faiss 未安装，请设置 VECTOR_STORE=numpy 或安装 faiss-cpu")

    def build(self, embeddings: np.ndarray, metadatas: List[Dict]) -> None:
        self._require_faiss()
        index = faiss.IndexFlatIP(self.dim)
        index.add(embeddings.astype(np.float32))
        self._index = index
        self._metas = metadatas
        faiss.write_index(self._index, str(self.index_path))
        with self.meta_path.open("w", encoding="utf-8") as f:
            for m in self._metas:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    def load(self) -> None:
        self._require_faiss()
        if self.index_path.exists():
            self._index = faiss.read_index(str(self.index_path))
        else:
            self._index = faiss.IndexFlatIP(self.dim)
        self._metas = []
        if self.meta_path.exists():
            with self.meta_path.open("r", encoding="utf-8") as f:
                for line in f:
                    self._metas.append(json.loads(line))

    @property
    def docs_count(self) -> int:
        return len(self._metas)

    def search(self, query_embedding: np.ndarray, top_k: int) -> List[Tuple[float, Dict]]:
        self._require_faiss()
        if self._index is None or self._index.ntotal == 0:
            return []
        D, I = self._index.search(query_embedding.reshape(1, -1).astype(np.float32), top_k)
        scores = D[0]
        idxs = I[0]
        results: List[Tuple[float, Dict]] = []
        for score, idx in zip(scores, idxs):
            if idx == -1:
                continue
            results.append((float(score), self._metas[int(idx)]))
        return results


