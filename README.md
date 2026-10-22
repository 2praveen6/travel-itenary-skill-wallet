## Deployment notes

For production deployments on Render or Vercel, set all required environment variables in the hosting platform before starting the app.

- Backend: `SECRET_KEY` or `JWT_SECRET` must be set to a strong secret value. Do not rely on the local development fallback.
- Backend: `FRONTEND_URL` (or `CLIENT_ORIGIN`) should point to the deployed frontend origin.
- Backend: `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are required when using Supabase.
- Backend: LLM credentials such as `GROQ_API_KEY`, `OPENAI_API_KEY`, or `HF_TOKEN` are needed for live AI itinerary generation.
- Frontend: use `VITE_API_URL` only when the app is not running locally behind the Vite proxy.

Avoid committing real `.env` files. Use the `.env.example` templates as the source of truth.
