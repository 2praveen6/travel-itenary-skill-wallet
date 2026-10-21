# Setup

## Local run

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Put the printed value in `backend/.env` as `SECRET_KEY` and `JWT_SECRET`.

```bash
uvicorn app.main:app --reload --port 5000
```

```bash
cd frontend
npm install
npm run dev
```

## API keys (optional, for live LLM itineraries)

1. **Groq** — https://console.groq.com/keys → Create API key → `GROQ_API_KEY`
2. **Hugging Face** — https://huggingface.co/settings/tokens → Read token `travel-planner` → `HF_TOKEN`
3. **Ollama** — install from https://ollama.com/download → `ollama pull llama3` → `LLM_PROVIDER=ollama`
4. **Supabase** — run `backend/database/schema.sql` then set `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`. If trip create returns `PGRST204` (missing column), run `backend/database/migrate_trips.sql` once in the SQL editor.

With no LLM keys the planner still generates curated rule-based itineraries.
