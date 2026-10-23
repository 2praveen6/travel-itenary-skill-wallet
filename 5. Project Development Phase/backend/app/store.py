from .config import using_supabase

if using_supabase():
    from . import supabase_repo as repo
else:
    from . import repository as repo

__all__ = ["repo"]
