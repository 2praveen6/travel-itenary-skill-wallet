# Architecture

```
React (Vite + Framer Motion + Lucide)
        |  tripsAPI / JWT
        v
FastAPI  (Pydantic request/response contracts)
        |-- prompt_builder.py  (role, constraints, injected prefs)
        |-- ai_engine.py       (OpenAI JSON or local curated engine)
        v
SQLite (dev) or Supabase schema (prod)
```

## Data

`profiles`, `preferences`, `trips`, `itinerary_days`, `activities`, `recommendation_logs`

The same table names are used in Postgres (`schema.sql`) and SQLite (`schema.sqlite.sql`).

## Recommendation

`buildRecommendationPrompt` turns preferences into a structured prompt. If `OPENAI_API_KEY` is set, the API asks the model for JSON destinations. Otherwise a local scorer ranks catalog cities by vibe, climate, budget tier, and companions.

## Itinerary

Catalog stops are filtered by vibe/interests, grouped into morning/afternoon/evening, ordered with nearest-neighbor on lat/lng, then given start/end times plus transfer minutes.
