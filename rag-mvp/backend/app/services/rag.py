from __future__ import annotations

from typing import Dict, List

from .llm import chat_completion


def build_prompt(question: str, contexts: List[Dict]) -> str:
    ctx_lines = []
    for i, c in enumerate(contexts, start=1):
        src = c.get("source", "")
        txt = c.get("text", "")
        ctx_lines.append(f"[{i}] 来源: {src}\n{txt}")
    ctx_block = "\n\n".join(ctx_lines) if ctx_lines else "(无上下文)"
    prompt = (
        "你将基于下方提供的餐饮知识上下文回答用户问题。\n"
        "要求：\n"
        "- 仅依据上下文回答，若上下文无答案，明确说明未找到并给出下一步建议。\n"
        "- 中文作答，先给结论，再列 2-3 条要点，最后标注命中的来源编号。\n\n"
        f"上下文：\n{ctx_block}\n\n"
        f"问题：{question}\n"
    )
    return prompt


def answer_question(question: str, contexts: List[Dict]) -> str:
    prompt = build_prompt(question, contexts)
    return chat_completion(prompt)


