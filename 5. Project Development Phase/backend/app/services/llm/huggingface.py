import httpx

from ...config import HF_MODEL, HF_TOKEN
from .base import LLMProvider, extract_message


class HuggingFaceProvider(LLMProvider):
    name = "huggingface"

    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        if not HF_TOKEN:
            raise RuntimeError("HF_TOKEN is not set")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient(timeout=90) as client:
            res = await client.post(
                "https://router.huggingface.co/v1/chat/completions",
                headers={"Authorization": f"Bearer {HF_TOKEN}"},
                json={"model": HF_MODEL, "temperature": 0.4, "messages": messages},
            )
            if res.status_code < 400:
                return extract_message(res.json())
            fallback = await client.post(
                f"https://api-inference.huggingface.co/models/{HF_MODEL}",
                headers={"Authorization": f"Bearer {HF_TOKEN}"},
                json={"inputs": f"{system or ''}\n\n{prompt}", "parameters": {"max_new_tokens": 1200}},
            )
        fallback.raise_for_status()
        data = fallback.json()
        if isinstance(data, list) and data:
            return data[0].get("generated_text") or str(data[0])
        return extract_message(data if isinstance(data, dict) else {})
