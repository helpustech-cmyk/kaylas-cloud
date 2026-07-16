import os
import re
from typing import Optional

import httpx
from fastapi import HTTPException

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

SYSTEM_PROMPT = """You are Kaylas AI, the digital twin of Kailas (Kaylas) Swami — Digital Revenue Lead at Quick Heal and a Process Automation Architect.

Your job is to answer questions about Kailas's work, his Service + AI philosophy, automation architecture (n8n, Python, Docker, AI agents), and how Indian businesses can cut operational costs.

Rules:
- Be practical, direct, and execution-first.
- Use Indian business context when relevant (INR, SMBs, hiring costs).
- Keep answers concise but useful.
- If you don't know, say so and offer to connect the visitor with Kailas.
- Never make up facts not supported by the provided context.
"""


def strip_thinking(text: str) -> str:
    # Remove common thinking tags if model emits them
    return re.sub(r"&lt;think&gt;.*?&lt;/think&gt;", "", text, flags=re.DOTALL).strip()


async def chat_with_ollama(messages: list[dict], model: Optional[str] = None) -> str:
    model = model or OLLAMA_MODEL
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.7, "num_ctx": 4096},
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            res = await client.post(f"{OLLAMA_HOST}/api/chat", json=payload)
            res.raise_for_status()
            data = res.json()
            return strip_thinking(data["message"]["content"].strip())
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Ollama error: {e}")


async def chat_with_groq(messages: list[dict], model: Optional[str] = None) -> str:
    if not GROQ_API_KEY:
        raise HTTPException(status_code=503, detail="Groq API key not configured")
    model = model or GROQ_MODEL
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            res = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json=payload,
            )
            res.raise_for_status()
            data = res.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Groq error: {e}")


async def generate_chat_response(messages: list[dict]) -> str:
    """Try Ollama first; fall back to Groq."""
    try:
        return await chat_with_ollama(messages)
    except Exception:
        if GROQ_API_KEY:
            return await chat_with_groq(messages)
        raise
