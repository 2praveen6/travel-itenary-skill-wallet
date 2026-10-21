import httpx

from ...config import OPENAI_API_KEY, OPENAI_MODEL
from .base import LLMProvider, extract_message


class OpenAIProvider(LLMProvider):
    name = "openai"

    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient(timeout=60) as client:
            res = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={"model": OPENAI_MODEL, "temperature": 0.4, "messages": messages},
            )
        res.raise_for_status()
        return extract_message(res.json())
