import httpx

from ...config import GROQ_API_KEY, GROQ_MODEL
from .base import LLMProvider, extract_message


class GroqProvider(LLMProvider):
    name = "groq"

    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY is not set")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient(timeout=60) as client:
            res = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                json={"model": GROQ_MODEL, "temperature": 0.4, "messages": messages},
            )
        res.raise_for_status()
        return extract_message(res.json())
