# Local setup

## Prerequisites

- Python 3.11 or newer
- Node.js 18 or newer
- A code editor

Optional: a [Supabase](https://supabase.com) project and a [Groq](https://console.groq.com/keys) API key. Without them the app still runs (SQLite + rule-based itineraries).

## Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate          # Windows
# source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
```

Create `backend/.env` from `.env.example`:

```bash
copy .env.example .env            # Windows
# cp .env.example .env            # macOS / Linux
```

Generate a signing secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Paste the value into `SECRET_KEY` and `JWT_SECRET`. Leave `FRONTEND_URL` as `http://localhost:5173`.

Start the API:

```bash
uvicorn app.main:app --reload --port 5000
```

Confirm `GET http://localhost:5000/api/health` returns `"status": "ok"`.

### Optional services

| Provider | Env var | Notes |
| --- | --- | --- |
| Groq | `GROQ_API_KEY` | Default live LLM |
| OpenAI | `OPENAI_API_KEY` | Used if Groq is empty |
| Hugging Face | `HF_TOKEN` | Inference token |
| Ollama | `OLLAMA_URL` | Local models only |
| Supabase | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` | Run `database/schema.sql` in the SQL editor first |

If the URL includes `/rest/v1`, remove that suffix. The backend normalizes it, but the project URL is the correct value.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173). The Vite dev server proxies `/api` to port 5000.

## First-run checklist

1. Register an account
2. Open **Explore** and save a ready-made trip, or use **Custom** to generate one
3. Open the itinerary, share it, and export Markdown if needed
