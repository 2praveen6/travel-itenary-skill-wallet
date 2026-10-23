import httpx

from ...config import OLLAMA_MODEL, OLLAMA_URL
from .base import LLMProvider, extract_message


class OllamaProvider(LLMProvider):
    name = "ollama"

    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient(timeout=120) as client:
            res = await client.post(
                f"{OLLAMA_URL.rstrip('/')}/api/chat",
                json={"model": OLLAMA_MODEL, "messages": messages, "stream": False, "format": "json"},
            )
        res.raise_for_status()
        return extract_message(res.json())
