import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def _env(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value.strip().strip('"').strip("'")
    return default


JWT_SECRET = _env("SECRET_KEY", "JWT_SECRET", default=secrets.token_hex(32))
JWT_ALGORITHM = "HS256"
CLIENT_ORIGIN = _env("FRONTEND_URL", "CLIENT_ORIGIN", default="http://localhost:5173")
PORT = int(os.getenv("PORT", "5000"))


def _normalize_supabase_url(url: str) -> str:
    url = (url or "").strip().rstrip("/")
    for suffix in ("/rest/v1", "/auth/v1"):
        if url.lower().endswith(suffix):
            url = url[: -len(suffix)]
    return url.rstrip("/")


SUPABASE_URL = _normalize_supabase_url(os.getenv("SUPABASE_URL", ""))
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "auto").lower()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
HF_TOKEN = _env("HF_TOKEN", "HUGGINGFACE_API_KEY", "HUGGINGFACEHUB_API_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

DATABASE_PATH = os.getenv("DATABASE_PATH", str(ROOT / "database" / "app.db"))
SCHEMA_PATH = ROOT / "database" / "schema.sqlite.sql"


def using_supabase() -> bool:
    return bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY)
