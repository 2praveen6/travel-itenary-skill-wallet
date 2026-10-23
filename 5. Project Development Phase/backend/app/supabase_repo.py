import re

from .db import dumps, new_id, now
from .supabase_client import get_service_client

_MISSING_COL = re.compile(r"Could not find the '([^']+)' column", re.I)


def sb():
    return get_service_client()


def _error_text(err: Exception) -> str:
    parts = [str(err)]
    for attr in ("message", "code", "details", "hint"):
        value = getattr(err, attr, None)
        if value:
            parts.append(str(value))
    if err.args:
        parts.append(str(err.args[0]))
    return " ".join(parts)


def _missing_column(err: Exception) -> str | None:
    match = _MISSING_COL.search(_error_text(err))
    return match.group(1) if match else None


def _write(table: str, payload: dict, method: str = "insert"):
    data = dict(payload)
    for _ in range(20):
        try:
            query = sb().table(table)
            if method == "upsert":
                return query.upsert(data).execute()
            return query.insert(data).execute()
        except Exception as err:
            column = _missing_column(err)
            if not column or column not in data:
                raise
            data.pop(column, None)
    raise RuntimeError(f"Could not write {table}: too many unknown columns")


def _insert(table: str, payload: dict | list):
    """Insert, dropping columns PostgREST does not know about (PGRST204)."""
    data = [dict(item) for item in payload] if isinstance(payload, list) else dict(payload)
    for _ in range(20):
        try:
            return sb().table(table).insert(data).execute()
        except Exception as err:
            column = _missing_column(err)
            if not column:
                raise
            if isinstance(data, list):
                if not any(column in row for row in data):
                    raise
                for row in data:
                    row.pop(column, None)
            else:
                if column not in data:
                    raise
                data.pop(column, None)
    raise RuntimeError(f"Could not insert into {table}: too many unknown columns")


def _trip_row(data: dict) -> dict:
    if not data:
        return data
    interests = data.get("interests") or []
    if isinstance(interests, str):
        from .db import loads

        interests = loads(interests)
    data["interests"] = interests
    for key in ("start_date", "end_date", "created_at", "updated_at"):
        if data.get(key) is not None:
            data[key] = str(data[key])
    return data


def create_user(name: str, email: str, password_hash: str) -> dict:
    user_id = new_id()
    created = now()
    client = sb()
    client.table("profiles").insert(
        {"id": user_id, "name": name, "email": email, "password_hash": password_hash, "created_at": created}
    ).execute()
    _insert("preferences", {"user_id": user_id})
    return {"id": user_id, "name": name, "email": email, "created_at": created}


def find_user_by_email(email: str):
    data = sb().table("profiles").select("*").eq("email", email).limit(1).execute().data
    return data[0] if data else None


def find_user_by_id(user_id: str):
    data = sb().table("profiles").select("id, name, email, created_at").eq("id", user_id).limit(1).execute().data
    return data[0] if data else None


def get_preferences(user_id: str):
    data = sb().table("preferences").select("*").eq("user_id", user_id).limit(1).execute().data
    return data[0] if data else None


def upsert_preferences(user_id: str, payload: dict) -> dict:
    current = get_preferences(user_id) or {"user_id": user_id}
    merged = {**current, **payload, "user_id": user_id, "updated_at": now()}
    if isinstance(merged.get("interests"), str):
        merged["interests"] = [p.strip() for p in merged["interests"].split(",") if p.strip()]
    _write("preferences", merged, "upsert")
    return get_preferences(user_id)


def list_trips(user_id: str) -> list[dict]:
    data = sb().table("trips").select("*").eq("user_id", user_id).order("created_at", desc=True).execute().data
    return [_trip_row(row) for row in (data or [])]


async def _noop():
    return None


def hydrate_trip(trip: dict | None) -> dict | None:
    if not trip:
        return None
    trip = _trip_row(dict(trip))
    days = sb().table("itinerary_days").select("*").eq("trip_id", trip["id"]).order("day_number").execute().data or []
    out = []
    for day in days:
        if day.get("date"):
            day["date"] = str(day["date"])
        acts = (
            sb().table("activities").select("*").eq("day_id", day["id"]).order("sort_order").execute().data or []
        )
        out.append({**day, "activities": acts})
    trip["days"] = out
    return trip


def get_trip(user_id: str, trip_id: str):
    data = sb().table("trips").select("*").eq("id", trip_id).eq("user_id", user_id).limit(1).execute().data
    return hydrate_trip(data[0] if data else None)


def insert_plan(trip_id: str, plan: list[dict]) -> None:
    for day in plan:
        day_id = new_id()
        _insert(
            "itinerary_days",
            {
                "id": day_id,
                "trip_id": trip_id,
                "day_number": day.get("day_number"),
                "date": day.get("date"),
                "theme": day.get("theme"),
                "summary": day.get("summary"),
            },
        )
        rows = []
        for idx, act in enumerate(day.get("activities") or []):
            rows.append(
                {
                    "id": new_id(),
                    "day_id": day_id,
                    "time_slot": act.get("time_slot") or "afternoon",
                    "start_time": act.get("start_time"),
                    "end_time": act.get("end_time"),
                    "title": act.get("title"),
                    "description": act.get("description"),
                    "location": act.get("location"),
                    "category": act.get("category"),
                    "vibe": act.get("vibe"),
                    "estimated_cost": act.get("estimated_cost") or 0,
                    "duration_minutes": act.get("duration_minutes"),
                    "travel_minutes": act.get("travel_minutes") or 0,
                    "sort_order": act.get("sort_order", idx),
                }
            )
        if rows:
            _insert("activities", rows)


def create_trip(user_id: str, payload: dict, plan: list[dict]) -> dict:
    trip_id = new_id()
    created = now()
    row = {
        "id": trip_id,
        "user_id": user_id,
        "title": payload.get("title") or f"{payload['destination']} trip",
        "destination_id": payload.get("destination_id"),
        "destination": payload["destination"],
        "start_date": str(payload["start_date"]),
        "end_date": str(payload["end_date"]),
        "budget": payload.get("budget"),
        "vibe": str(payload.get("vibe") or payload.get("travel_style") or "culture"),
        "interests": payload.get("interests") or [],
        "notes": payload.get("notes"),
        "travelers": payload.get("travelers") or 1,
        "dietary": payload.get("dietary"),
        "mobility": payload.get("mobility"),
        "pace": str(payload.get("pace") or "moderate"),
        "travel_style": str(payload.get("travel_style") or payload.get("vibe") or "culture"),
        "companions": payload.get("companions") or "solo",
        "created_at": created,
        "updated_at": created,
    }
    _insert("trips", row)
    insert_plan(trip_id, plan)
    return get_trip(user_id, trip_id)


def replace_plan(user_id: str, trip_id: str, plan: list[dict]):
    days = sb().table("itinerary_days").select("id").eq("trip_id", trip_id).execute().data or []
    for day in days:
        sb().table("activities").delete().eq("day_id", day["id"]).execute()
    sb().table("itinerary_days").delete().eq("trip_id", trip_id).execute()
    insert_plan(trip_id, plan)
    sb().table("trips").update({"updated_at": now()}).eq("id", trip_id).execute()
    return get_trip(user_id, trip_id)


def update_trip(user_id: str, trip_id: str, patch: dict):
    trip = get_trip(user_id, trip_id)
    if not trip:
        return None
    sb().table("trips").update(
        {
            "title": patch.get("title") or trip["title"],
            "notes": patch.get("notes", trip.get("notes")),
            "budget": patch.get("budget", trip.get("budget")),
            "updated_at": now(),
        }
    ).eq("id", trip_id).execute()
    return get_trip(user_id, trip_id)


def delete_trip(user_id: str, trip_id: str) -> bool:
    trip = get_trip(user_id, trip_id)
    if not trip:
        return False
    for day in trip["days"]:
        sb().table("activities").delete().eq("day_id", day["id"]).execute()
    sb().table("itinerary_days").delete().eq("trip_id", trip_id).execute()
    sb().table("trips").delete().eq("id", trip_id).execute()
    return True


def add_activity(user_id: str, trip_id: str, day_id: str, payload: dict):
    trip = get_trip(user_id, trip_id)
    if not trip:
        return None
    day = next((d for d in trip["days"] if d["id"] == day_id), None)
    if not day:
        return False
    act_id = new_id()
    row = {
        "id": act_id,
        "day_id": day_id,
        "time_slot": payload.get("time_slot") or "afternoon",
        "start_time": payload.get("start_time"),
        "title": payload["title"],
        "description": payload.get("description"),
        "location": payload.get("location"),
        "category": payload.get("category"),
        "estimated_cost": payload.get("estimated_cost") or 0,
        "sort_order": len(day["activities"]),
    }
    _insert("activities", row)
    return row


def delete_activity(user_id: str, trip_id: str, activity_id: str) -> bool:
    trip = get_trip(user_id, trip_id)
    if not trip:
        return False
    found = any(a["id"] == activity_id for d in trip["days"] for a in d["activities"])
    if not found:
        return False
    sb().table("activities").delete().eq("id", activity_id).execute()
    return True


def log_recommendation(user_id: str, prompt: str, result) -> None:
    sb().table("recommendation_logs").insert(
        {"id": new_id(), "user_id": user_id, "prompt": prompt, "result": result if isinstance(result, (dict, list)) else dumps(result)}
    ).execute()


def enable_share(user_id: str, trip_id: str) -> dict | None:
    trip = get_trip(user_id, trip_id)
    if not trip:
        return None
    token = trip.get("share_token") or new_id()
    sb().table("trips").update({"share_token": token, "updated_at": now()}).eq("id", trip_id).execute()
    trip["share_token"] = token
    return trip


def get_trip_by_share_token(token: str):
    data = sb().table("trips").select("*").eq("share_token", token).limit(1).execute().data
    return hydrate_trip(data[0] if data else None)
