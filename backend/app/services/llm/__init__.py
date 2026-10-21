from ...config import GROQ_API_KEY, HF_TOKEN, LLM_PROVIDER, OPENAI_API_KEY
from .base import LLMProvider
from .groq import GroqProvider
from .huggingface import HuggingFaceProvider
from .ollama import OllamaProvider
from .openai_provider import OpenAIProvider

PROVIDERS = {
    "groq": GroqProvider,
    "openai": OpenAIProvider,
    "huggingface": HuggingFaceProvider,
    "hf": HuggingFaceProvider,
    "ollama": OllamaProvider,
}


def available_provider() -> LLMProvider | None:
    if LLM_PROVIDER not in {"", "auto"} and LLM_PROVIDER in PROVIDERS:
        return PROVIDERS[LLM_PROVIDER]()
    if GROQ_API_KEY:
        return GroqProvider()
    if OPENAI_API_KEY:
        return OpenAIProvider()
    if HF_TOKEN:
        return HuggingFaceProvider()
    if LLM_PROVIDER == "ollama":
        return OllamaProvider()
    return None


__all__ = ["LLMProvider", "available_provider"]
