# Architecture

Waypoint is a small three-tier app: a React SPA, a FastAPI service, and either Supabase Postgres or local SQLite.

```
React (Vite)
  tripsAPI · JWT in localStorage
        │
        ▼
FastAPI
  ├── auth / preferences / trips / templates
  ├── prompt_builder.py     structured LLM prompts
  ├── ai_engine.py          Groq → OpenAI → HF → Ollama → rules
  ├── services/templates.py ready-made itineraries
  └── optimize.py           cluster stops and fill transfer times
        │
        ▼
Supabase (prod)  or  SQLite (dev)
```

## Data model

| Table | Role |
| --- | --- |
| `profiles` | Users (email + password hash) |
| `preferences` | Vibe, budget, companions, dietary notes |
| `trips` | One planned journey |
| `itinerary_days` | Day theme, date, summary |
| `activities` | Timed stops (stay, food, attraction, transport) |
| `recommendation_logs` | Prompt / result audit |

Schemas: [`backend/database/schema.sql`](backend/database/schema.sql) (Postgres) and [`backend/database/schema.sqlite.sql`](backend/database/schema.sqlite.sql).

## Planning pipeline

1. Collect traveler inputs (or clone a template)
2. Build a constrained JSON prompt from preferences
3. Ask the first available LLM for a day list
4. If the model fails, assemble days from the destination catalog
5. Optimize walking order and attach stay + transport rows
6. Persist via the Supabase service role (or SQLite)

## Auth

Registration and login issue a JWT. The browser sends `Authorization: Bearer <token>`. Public share pages use `GET /api/share/{token}` with no auth.
