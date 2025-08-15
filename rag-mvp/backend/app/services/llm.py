from __future__ import annotations

import os
from typing import Dict, List

import requests

from ..config import get_settings


def chat_completion(prompt: str) -> str:
    settings = get_settings()
    provider = settings.llm_provider.lower()
    if provider == "openai":
        return _chat_openai(prompt)
    if provider == "ollama":
        return _generate_ollama(prompt)
    if provider == "dashscope":
        return _chat_dashscope(prompt)
    raise ValueError(f"不支持的 LLM_PROVIDER: {provider}")


def _chat_openai(prompt: str) -> str:
    s = get_settings()
    url = f"{s.openai_base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {s.openai_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": s.openai_model,
        "messages": [
            {"role": "system", "content": "你是一个严格基于提供上下文回答的餐饮行业助手，未命中上下文时请明确说明。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    resp.raise_for_status()
    j = resp.json()
    return j["choices"][0]["message"]["content"].strip()


def _generate_ollama(prompt: str) -> str:
    s = get_settings()
    url = f"{s.ollama_base_url.rstrip('/')}/api/generate"
    data = {"model": s.ollama_model, "prompt": prompt, "stream": False}
    resp = requests.post(url, json=data, timeout=120)
    resp.raise_for_status()
    j = resp.json()
    return (j.get("response") or "").strip()


def _chat_dashscope(prompt: str) -> str:
    # 简化实现：使用通义统一聊天接口
    s = get_settings()
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {s.dashscope_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": s.dashscope_model,
        "messages": [
            {"role": "system", "content": "你是一个严格基于提供上下文回答的餐饮行业助手，未命中上下文时请明确说明。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    resp.raise_for_status()
    j = resp.json()
    return j["choices"][0]["message"]["content"].strip()


