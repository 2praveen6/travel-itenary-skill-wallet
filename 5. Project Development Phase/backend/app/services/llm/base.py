from abc import ABC, abstractmethod
import json
import re


class LLMProvider(ABC):
    """Standard interface for Groq, Hugging Face, Ollama, and OpenAI."""

    name: str = "base"

    @abstractmethod
    async def generate(self, prompt: str, *, system: str | None = None) -> str:
        raise NotImplementedError

    async def generate_json(self, prompt: str, *, system: str | None = None) -> dict:
        text = await self.generate(prompt, system=system or "Return valid JSON only. No markdown.")
        cleaned = re.sub(r"```json|```", "", text).strip()
        return json.loads(cleaned)


def extract_message(payload: dict) -> str:
    if payload.get("choices"):
        return payload["choices"][0]["message"]["content"]
    if payload.get("message"):
        return payload["message"].get("content") or ""
    return payload.get("generated_text") or payload.get("response") or ""
