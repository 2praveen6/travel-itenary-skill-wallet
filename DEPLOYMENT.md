# Deployment

Production layout:

- **API** — Render (FastAPI + Gunicorn)
- **Frontend** — Vercel (Vite static build)
- **Database** — Supabase Postgres

Connect both services to [this GitHub repository](https://github.com/2praveen6/travel-itenary-skill-wallet). Do not upload `.env` files.

## 1. Supabase

1. Create a project
2. Run [`backend/database/schema.sql`](backend/database/schema.sql) in the SQL editor
3. If you already had an older `trips` table, also run [`backend/database/migrate_trips.sql`](backend/database/migrate_trips.sql)
4. Copy the project URL and **service role** key

## 2. Backend on Render

1. New → Web Service → this GitHub repo
2. **Root directory:** `backend`
3. **Build:** `pip install -r requirements.txt`
4. **Start:** `gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
5. Set environment variables (use Render’s generate for secrets):

| Key | Value |
| --- | --- |
| `SECRET_KEY` | generated |
| `JWT_SECRET` | generated |
| `FRONTEND_URL` | Vercel URL (set after step 3, then redeploy) |
| `CLIENT_ORIGIN` | same as `FRONTEND_URL` |
| `SUPABASE_URL` | `https://xxxx.supabase.co` |
| `SUPABASE_ANON_KEY` | anon key |
| `SUPABASE_SERVICE_ROLE_KEY` | service role key |
| `GROQ_API_KEY` | Groq key |
| `LLM_PROVIDER` | `auto` |

6. Deploy and copy the `*.onrender.com` URL. Check `/api/health`.

A [`render.yaml`](render.yaml) blueprint is included if you prefer Infrastructure-as-Code.

## 3. Frontend on Vercel

1. New Project → this GitHub repo
2. **Root directory:** `frontend`
3. Framework: Vite · output: `dist` · install: `npm install` · build: `npm run build`
4. Environment variable:

```
VITE_API_URL=https://YOUR-SERVICE.onrender.com
```

No trailing slash. The client already prefixes `/api`.

5. Deploy, copy the Vercel HTTPS URL
6. Put that URL into Render `FRONTEND_URL` and `CLIENT_ORIGIN`, then redeploy the API so CORS and share links work

## 4. Smoke test

- Open the Vercel URL
- Register, save a ready-made itinerary, generate a custom trip
- Confirm share links use the production frontend origin
