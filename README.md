# Personalized Travel Itinerary Planner

Full-stack AI travel planner: **React** UI, **FastAPI** API, **Supabase** storage, and **Groq** (or Hugging Face / Ollama) for generated itineraries.

Enter destination, dates, budget, group size, and style. The app returns a timed day-by-day plan with attractions, dining, a stay suggestion, and local transport — then you can save, edit, share, or regenerate.

## Who it is for

1. **Solo weekend** — food and sightseeing, tight time, walking-order days.
2. **Couple trip** — relaxed pace, scenic stays, premium dining, collaborative refine.
3. **Friends group** — traveler count, mixed interests, shared link, one budget.

## Run locally

```bash
cd backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload --port 5000
```

```bash
cd frontend
npm run dev
```

Open http://localhost:5173 · API docs http://localhost:5000/docs

Keys live in `backend/.env` (never commit). See [SETUP.md](SETUP.md) and [DEPLOYMENT.md](DEPLOYMENT.md).

## GitHub

This folder is the repo root. Do not commit `backend/.env`. Copy `backend/.env.example` and `frontend/.env.example` instead.

```bash
git init
git add .
git status   # confirm .env is not listed
git commit -m "Initial Waypoint travel planner"
```

Then create an empty GitHub repo and `git remote add origin …` + `git push -u origin main`.

Deploy next: backend on Render (`render.yaml`, root `backend`), frontend on Vercel (`frontend/vercel.json`, env `VITE_API_URL`).
