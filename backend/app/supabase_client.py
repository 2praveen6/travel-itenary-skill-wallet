"""Centralized Supabase access for FastAPI routes and services."""

from functools import lru_cache

from .config import SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL, using_supabase


def _create(key: str):
    if not using_supabase() or not key:
        raise RuntimeError("Supabase is not configured. Set SUPABASE_URL and keys in .env")
    from supabase import create_client

    return create_client(SUPABASE_URL, key)


@lru_cache(maxsize=1)
def get_client():
    """Public/anon client for user-scoped operations."""
    return _create(SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY)


@lru_cache(maxsize=1)
def get_service_client():
    """Service-role client for elevated backend CRUD (bypasses RLS)."""
    return _create(SUPABASE_SERVICE_ROLE_KEY)
