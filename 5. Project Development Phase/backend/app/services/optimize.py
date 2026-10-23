"""Geographic ordering and time-slot assignment for daily itineraries."""

from math import asin, cos, radians, sin, sqrt


def haversine_km(a: dict, b: dict) -> float:
    if a.get("lat") is None or b.get("lat") is None:
        return 1.2
    lat1, lon1, lat2, lon2 = map(radians, [a["lat"], a["lng"], b["lat"], b["lng"]])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(min(1, sqrt(h)))


def travel_minutes(a: dict, b: dict) -> int:
    return max(8, round(haversine_km(a, b) / 12 * 60))


def add_minutes(hhmm: str, minutes: int) -> str:
    hours, mins = [int(part) for part in hhmm.split(":")]
    total = (hours * 60 + mins + minutes) % (24 * 60)
    return f"{total // 60:02d}:{total % 60:02d}"


def nearest_neighbor(items: list[dict]) -> list[dict]:
    if len(items) <= 2:
        return items
    remaining = list(items)
    ordered = [remaining.pop(0)]
    while remaining:
        last = ordered[-1]
        remaining.sort(key=lambda item: haversine_km(last, item))
        ordered.append(remaining.pop(0))
    return ordered


def jitter_coords(activity: dict, fallback: dict | None) -> dict:
    if activity.get("lat") is not None:
        return activity
    base_lat = (fallback or {}).get("lat") or 0
    base_lng = (fallback or {}).get("lng") or 0
    seed = abs(hash(activity.get("location") or activity.get("title") or "x")) % 100
    activity = dict(activity)
    activity["lat"] = base_lat + (seed - 50) * 0.002
    activity["lng"] = base_lng + ((seed * 7) % 100 - 50) * 0.002
    return activity


def optimize_day(activities: list[dict], pace: str = "moderate", place: dict | None = None) -> list[dict]:
    grouped = {"morning": [], "afternoon": [], "evening": []}
    for activity in activities:
        slot = activity.get("time_slot") if activity.get("time_slot") in grouped else "afternoon"
        grouped[slot].append(jitter_coords(activity, place))
    if pace in {"relaxed", "slow"}:
        grouped["afternoon"] = grouped["afternoon"][:1]
    cursor = "09:00"
    ordered = []
    for slot in ("morning", "afternoon", "evening"):
        stops = nearest_neighbor(grouped[slot])
        for index, activity in enumerate(stops):
            if index == 0 and slot == "afternoon":
                cursor = max(cursor, "13:00")
            if index == 0 and slot == "evening":
                cursor = max(cursor, "18:00")
            prev = ordered[-1] if ordered else None
            transfer = travel_minutes(prev, activity) if prev else 0
            cursor = add_minutes(cursor, transfer)
            start = cursor
            duration = activity.get("duration_minutes") or 90
            end = add_minutes(start, duration)
            ordered.append(
                {
                    **activity,
                    "time_slot": slot,
                    "start_time": start,
                    "end_time": end,
                    "travel_minutes": transfer,
                    "sort_order": len(ordered),
                }
            )
            cursor = end
    return ordered


def optimize_plan(plan: list[dict], pace: str = "moderate", place: dict | None = None) -> list[dict]:
    out = []
    for day in plan:
        activities = optimize_day(day.get("activities") or [], pace, place)
        out.append({**day, "activities": activities})
    return out
