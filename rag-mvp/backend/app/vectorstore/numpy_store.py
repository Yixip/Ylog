from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np


@dataclass
class NumpyStore:
    index_dir: Path

    def __post_init__(self) -> None:
        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.emb_path = self.index_dir / "embeddings.npy"
        self.meta_path = self.index_dir / "meta.jsonl"
        self._embeddings: np.ndarray | None = None
        self._metas: List[Dict] = []

    def build(self, embeddings: np.ndarray, metadatas: List[Dict]) -> None:
        self._embeddings = embeddings.astype(np.float32)
        self._metas = metadatas
        np.save(self.emb_path, self._embeddings)
        with self.meta_path.open("w", encoding="utf-8") as f:
            for m in self._metas:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    def load(self) -> None:
        if self.emb_path.exists():
            self._embeddings = np.load(self.emb_path)
        else:
            self._embeddings = np.zeros((0, 1), dtype=np.float32)
        self._metas = []
        if self.meta_path.exists():
            with self.meta_path.open("r", encoding="utf-8") as f:
                for line in f:
                    self._metas.append(json.loads(line))

    @property
    def docs_count(self) -> int:
        return len(self._metas)

    def search(self, query_embedding: np.ndarray, top_k: int) -> List[Tuple[float, Dict]]:
        if self._embeddings is None or len(self._embeddings) == 0:
            return []
        q = query_embedding.astype(np.float32)
        sims = self._embeddings @ q  # 归一化后内积即余弦相似度
        idx = np.argsort(-sims)[:top_k]
        results: List[Tuple[float, Dict]] = []
        for i in idx:
            results.append((float(sims[i]), self._metas[int(i)]))
        return results


