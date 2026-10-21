# Project completion

The stack is React + FastAPI + Supabase/SQLite + Groq (with Hugging Face / Ollama fallback). The leftover Node Express API is removed.

| Area | Status |
| --- | --- |
| Auth, dashboard, trip CRUD | Done |
| Multi-step trip builder (solo / couple / group) | `/plan` |
| Preferences + destination recommendations | `/preferences`, `/recommend` |
| AI day-by-day itinerary (stay, dining, sights, transport) | `POST /api/trips` |
| Route/time optimization | `app/services/optimize.py` |
| Refine whole trip or one day | `/trips/{id}/refine` |
| Share + export JSON / Markdown / ICS | `/share/:token` |
| Deploy | Render API (`render.yaml`) + Vercel frontend |

## Scenarios covered

1. **Solo weekend** — 1 traveler, food/sightseeing interests, budget, walking-order days.
2. **Couple vacation** — couple + relaxed/romance style, boutique stay, refine together.
3. **Friends group** — traveler count, mixed interests, shared link, cost vs budget on the itinerary.

## Checks

1. Register and log in
2. Build a trip for each companion type
3. Confirm stay + dining + transport on the itinerary
4. Share the group trip and export Markdown/ICS
5. `GET /api/health` shows `supabase` or `sqlite` and the LLM provider
