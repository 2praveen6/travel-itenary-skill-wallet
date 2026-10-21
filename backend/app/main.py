from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import CLIENT_ORIGIN, using_supabase
from .db import init_db
from .routers import auth, preferences, templates, trips
from .services.destinations import CATALOG
from .services.llm import available_provider
from .store import repo

if not using_supabase():
    init_db()

app = FastAPI(
    title="Personalized Travel Itinerary Planner",
    version="3.0.1",
    description="FastAPI + LLM providers (Groq/HF/Ollama) + Supabase/SQLite.",
)

origins = list({CLIENT_ORIGIN, "http://localhost:5173", "http://127.0.0.1:5173"})
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(preferences.router, prefix="/api")
app.include_router(trips.router, prefix="/api")
app.include_router(templates.router, prefix="/api")


@app.get("/")
def root():
    return {"service": "personalized-travel-itinerary-planner", "docs": "/docs", "api": "/api/health"}


@app.get("/api/health")
def health():
    provider = available_provider()
    return {
        "status": "ok",
        "service": "fastapi-travel-itinerary",
        "database": "supabase" if using_supabase() else "sqlite",
        "llm": provider.name if provider else "rules",
    }


@app.get("/api/destinations")
def destinations():
    return [{k: v for k, v in place.items() if k != "activities"} for place in CATALOG]


@app.get("/api/share/{token}")
def public_share(token: str):
    trip = repo.get_trip_by_share_token(token)
    if not trip:
        raise HTTPException(status_code=404, detail="Shared itinerary not found")
    return trip


@app.exception_handler(HTTPException)
async def http_error(_request: Request, exc: HTTPException):
    message = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"error": message})


@app.exception_handler(RequestValidationError)
async def validation_error(_request: Request, exc: RequestValidationError):
    first = exc.errors()[0] if exc.errors() else {"msg": "Invalid request"}
    loc = ".".join(str(part) for part in first.get("loc", []) if part != "body")
    return JSONResponse(status_code=422, content={"error": f"{loc}: {first.get('msg', 'invalid')}".strip(": ")})


@app.exception_handler(Exception)
async def unhandled_error(_request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"error": str(exc) or "Unexpected server error"})
