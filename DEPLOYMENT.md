# Deployment

Backend = **Render** (FastAPI). Frontend = **Vercel** (Vite). Database = **Supabase**.

## Backend on Render

1. Add New → Web Service → import GitHub repo
2. Root Directory: `backend`
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
5. Environment variables from `backend/.env.example` (`SECRET_KEY`/`JWT_SECRET`, `FRONTEND_URL`, Supabase, `GROQ_API_KEY` or `HF_TOKEN`)
6. Deploy and copy the `*.onrender.com` URL

## Frontend on Vercel

1. Add New → Project → import repo
2. Root Directory: `frontend`
3. Build: `npm run build` · Output: `dist` · Install: `npm install`
4. Env: `VITE_API_URL=https://YOUR-SERVICE.onrender.com`  
   (no trailing slash; the app already prefixes `/api`)
5. Deploy, copy the Vercel HTTPS URL
6. Set Render `FRONTEND_URL` (and `CLIENT_ORIGIN`) to that URL, then redeploy the API for CORS

## Groq / Hugging Face / Ollama keys

Do not commit keys. Create them in the provider dashboards and paste into Render env:

- Groq: https://console.groq.com/keys
- Hugging Face: https://huggingface.co/settings/tokens (Read token named `travel-planner`)
- Ollama local only: `ollama pull llama3` then `OLLAMA_URL=http://127.0.0.1:11434`
