from .db import connect, dumps, loads, new_id, now, row_to_dict


def create_user(name: str, email: str, password_hash: str) -> dict:
    user_id = new_id()
    created = now()
    conn = connect()
    conn.execute(
        "INSERT INTO profiles (id, name, email, password_hash, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, name, email, password_hash, created),
    )
    conn.execute(
        """INSERT INTO preferences (user_id, currency, vibe, companions, interests, pace, travelers, updated_at)
           VALUES (?, 'USD', 'culture', 'solo', '[]', 'moderate', 1, ?)""",
        (user_id, created),
    )
    conn.commit()
    conn.close()
    return {"id": user_id, "name": name, "email": email, "created_at": created}


def find_user_by_email(email: str):
    conn = connect()
    row = conn.execute("SELECT * FROM profiles WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None


def find_user_by_id(user_id: str):
    conn = connect()
    row = conn.execute("SELECT id, name, email, created_at FROM profiles WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_preferences(user_id: str):
    conn = connect()
    row = conn.execute("SELECT * FROM preferences WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return row_to_dict(row)


def upsert_preferences(user_id: str, payload: dict) -> dict:
    current = get_preferences(user_id) or {}
    merged = {
        "budget_min": payload.get("budget_min", current.get("budget_min")),
        "budget_max": payload.get("budget_max", current.get("budget_max")),
        "currency": payload.get("currency", current.get("currency") or "USD"),
        "vibe": payload.get("vibe", current.get("vibe") or "culture"),
        "climate": payload.get("climate", current.get("climate")),
        "companions": payload.get("companions", current.get("companions") or "solo"),
        "interests": dumps(payload.get("interests", current.get("interests"))),
        "pace": payload.get("pace", current.get("pace") or "moderate"),
        "dietary": payload.get("dietary", current.get("dietary")),
        "mobility": payload.get("mobility", current.get("mobility")),
        "season": payload.get("season", current.get("season")),
        "travelers": payload.get("travelers", current.get("travelers") or 1),
    }
    conn = connect()
    conn.execute(
        """INSERT INTO preferences (user_id, budget_min, budget_max, currency, vibe, climate, companions, interests, pace, dietary, mobility, season, travelers, updated_at)
           VALUES (:user_id, :budget_min, :budget_max, :currency, :vibe, :climate, :companions, :interests, :pace, :dietary, :mobility, :season, :travelers, :updated)
           ON CONFLICT(user_id) DO UPDATE SET
             budget_min=excluded.budget_min, budget_max=excluded.budget_max, currency=excluded.currency,
             vibe=excluded.vibe, climate=excluded.climate, companions=excluded.companions, interests=excluded.interests,
             pace=excluded.pace, dietary=excluded.dietary, mobility=excluded.mobility, season=excluded.season,
             travelers=excluded.travelers, updated_at=excluded.updated_at""",
        {"user_id": user_id, **merged, "updated": now()},
    )
    conn.commit()
    conn.close()
    return get_preferences(user_id)


def list_trips(user_id: str) -> list[dict]:
    conn = connect()
    rows = conn.execute("SELECT * FROM trips WHERE user_id = ? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return [row_to_dict(r) for r in rows]


def hydrate_trip(trip: dict | None) -> dict | None:
    if not trip:
        return None
    conn = connect()
    days = conn.execute("SELECT * FROM itinerary_days WHERE trip_id = ? ORDER BY day_number", (trip["id"],)).fetchall()
    out_days = []
    for day in days:
        acts = conn.execute("SELECT * FROM activities WHERE day_id = ? ORDER BY sort_order", (day["id"],)).fetchall()
        out_days.append({**dict(day), "activities": [dict(a) for a in acts]})
    conn.close()
    trip = row_to_dict(trip) if not isinstance(trip.get("interests"), list) else trip
    trip["days"] = out_days
    return trip


def get_trip(user_id: str, trip_id: str):
    conn = connect()
    row = conn.execute("SELECT * FROM trips WHERE id = ? AND user_id = ?", (trip_id, user_id)).fetchone()
    conn.close()
    return hydrate_trip(dict(row) if row else None)


def insert_plan(conn, trip_id: str, plan: list[dict]) -> None:
    for day in plan:
        day_id = new_id()
        conn.execute(
            "INSERT INTO itinerary_days (id, trip_id, day_number, date, theme, summary) VALUES (?, ?, ?, ?, ?, ?)",
            (day_id, trip_id, day.get("day_number"), day.get("date"), day.get("theme"), day.get("summary")),
        )
        for idx, act in enumerate(day.get("activities") or []):
            conn.execute(
                """INSERT INTO activities (id, day_id, time_slot, start_time, end_time, title, description, location, category, vibe, estimated_cost, duration_minutes, travel_minutes, sort_order)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    new_id(),
                    day_id,
                    act.get("time_slot") or "afternoon",
                    act.get("start_time"),
                    act.get("end_time"),
                    act.get("title"),
                    act.get("description"),
                    act.get("location"),
                    act.get("category"),
                    act.get("vibe"),
                    act.get("estimated_cost") or 0,
                    act.get("duration_minutes"),
                    act.get("travel_minutes") or 0,
                    act.get("sort_order", idx),
                ),
            )


def create_trip(user_id: str, payload: dict, plan: list[dict]) -> dict:
    trip_id = new_id()
    created = now()
    conn = connect()
    conn.execute(
        """INSERT INTO trips (id, user_id, title, destination_id, destination, start_date, end_date, budget, vibe, interests, notes, created_at, updated_at, travelers, dietary, mobility, pace, travel_style, companions)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            trip_id,
            user_id,
            payload.get("title") or f"{payload['destination']} trip",
            payload.get("destination_id"),
            payload["destination"],
            str(payload["start_date"]),
            str(payload["end_date"]),
            payload.get("budget"),
            str(payload.get("vibe") or payload.get("travel_style") or "culture"),
            dumps(payload.get("interests")),
            payload.get("notes"),
            created,
            created,
            payload.get("travelers") or 1,
            payload.get("dietary"),
            payload.get("mobility"),
            str(payload.get("pace") or "moderate"),
            str(payload.get("travel_style") or payload.get("vibe") or "culture"),
            payload.get("companions") or "solo",
        ),
    )
    insert_plan(conn, trip_id, plan)
    conn.commit()
    conn.close()
    return get_trip(user_id, trip_id)


def replace_plan(user_id: str, trip_id: str, plan: list[dict]):
    conn = connect()
    days = conn.execute("SELECT id FROM itinerary_days WHERE trip_id = ?", (trip_id,)).fetchall()
    for day in days:
        conn.execute("DELETE FROM activities WHERE day_id = ?", (day["id"],))
    conn.execute("DELETE FROM itinerary_days WHERE trip_id = ?", (trip_id,))
    insert_plan(conn, trip_id, plan)
    conn.execute("UPDATE trips SET updated_at = ? WHERE id = ?", (now(), trip_id))
    conn.commit()
    conn.close()
    return get_trip(user_id, trip_id)


def update_trip(user_id: str, trip_id: str, patch: dict):
    trip = get_trip(user_id, trip_id)
    if not trip:
        return None
    conn = connect()
    conn.execute(
        "UPDATE trips SET title = ?, notes = ?, budget = ?, updated_at = ? WHERE id = ?",
        (patch.get("title") or trip["title"], patch.get("notes", trip.get("notes")), patch.get("budget", trip.get("budget")), now(), trip_id),
    )
    conn.commit()
    conn.close()
    return get_trip(user_id, trip_id)


def delete_trip(user_id: str, trip_id: str) -> bool:
    trip = get_trip(user_id, trip_id)
    if not trip:
        return False
    conn = connect()
    for day in trip["days"]:
        conn.execute("DELETE FROM activities WHERE day_id = ?", (day["id"],))
    conn.execute("DELETE FROM itinerary_days WHERE trip_id = ?", (trip_id,))
    conn.execute("DELETE FROM trips WHERE id = ?", (trip_id,))
    conn.commit()
    conn.close()
    return True


def add_activity(user_id: str, trip_id: str, day_id: str, payload: dict):
    trip = get_trip(user_id, trip_id)
    if not trip:
        return None
    day = next((d for d in trip["days"] if d["id"] == day_id), None)
    if not day:
        return False
    act_id = new_id()
    conn = connect()
    conn.execute(
        """INSERT INTO activities (id, day_id, time_slot, start_time, title, description, location, category, estimated_cost, sort_order)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            act_id,
            day_id,
            payload.get("time_slot") or "afternoon",
            payload.get("start_time"),
            payload["title"],
            payload.get("description"),
            payload.get("location"),
            payload.get("category"),
            payload.get("estimated_cost") or 0,
            len(day["activities"]),
        ),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM activities WHERE id = ?", (act_id,)).fetchone()
    conn.close()
    return dict(row)


def delete_activity(user_id: str, trip_id: str, activity_id: str) -> bool:
    trip = get_trip(user_id, trip_id)
    if not trip:
        return False
    found = any(a["id"] == activity_id for d in trip["days"] for a in d["activities"])
    if not found:
        return False
    conn = connect()
    conn.execute("DELETE FROM activities WHERE id = ?", (activity_id,))
    conn.commit()
    conn.close()
    return True


def enable_share(user_id: str, trip_id: str) -> dict | None:
    trip = get_trip(user_id, trip_id)
    if not trip:
        return None
    token = trip.get("share_token") or new_id()
    conn = connect()
    conn.execute("UPDATE trips SET share_token = ?, updated_at = ? WHERE id = ?", (token, now(), trip_id))
    conn.commit()
    conn.close()
    trip["share_token"] = token
    return trip


def get_trip_by_share_token(token: str):
    conn = connect()
    row = conn.execute("SELECT * FROM trips WHERE share_token = ?", (token,)).fetchone()
    conn.close()
    return hydrate_trip(dict(row) if row else None)


def log_recommendation(user_id: str, prompt: str, result) -> None:
    conn = connect()
    conn.execute(
        "INSERT INTO recommendation_logs (id, user_id, prompt, result, created_at) VALUES (?, ?, ?, ?, ?)",
        (new_id(), user_id, prompt, dumps(result) if not isinstance(result, str) else result, now()),
    )
    conn.commit()
    conn.close()
