from __future__ import annotations

from typing import List


def split_text(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> List[str]:
    if not text:
        return []
    chunk_size = max(1, chunk_size)
    chunk_overlap = max(0, min(chunk_overlap, chunk_size - 1))

    chunks: List[str] = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        if end == length:
            break
        start = end - chunk_overlap
    return chunks


