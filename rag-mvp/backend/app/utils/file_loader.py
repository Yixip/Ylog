from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

from pypdf import PdfReader
from docx import Document


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _read_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n".join(texts)


def _read_docx(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)


def iter_documents(raw_dir: Path) -> Iterable[Dict]:
    exts = {".txt", ".md", ".pdf", ".docx"}
    for path in raw_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in exts:
            try:
                if path.suffix.lower() in {".txt", ".md"}:
                    txt = _read_text_file(path)
                elif path.suffix.lower() == ".pdf":
                    txt = _read_pdf(path)
                else:
                    txt = _read_docx(path)
                yield {"text": txt, "source": str(path.relative_to(raw_dir))}
            except Exception:
                continue


