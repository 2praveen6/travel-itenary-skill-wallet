from ..schemas import enum_text
from . import destinations as dest_mod
from .llm import available_provider
from .optimize import optimize_plan
from .prompt_builder import build_itinerary_prompt, build_recommendation_prompt, _days, build_system_role


async def complete_json(prompt: str) -> dict | None:
    provider = available_provider()
    if not provider:
        return None
    try:
        return await provider.generate_json(prompt, system=build_system_role())
    except Exception:
        return None


def score_place(place: dict, prefs: dict) -> float:
    score = 40
    vibe = enum_text(prefs.get("vibe") or prefs.get("travel_style")).lower()
    climate = str(prefs.get("climate") or "").lower()
    if vibe and vibe in place["vibes"]:
        score += 28
    if climate and climate in place["climates"]:
        score += 14
    interests = prefs.get("interests") or []
    for interest in interests:
        blob = " ".join(place["vibes"] + [place["summary"]]).lower()
        if str(interest).lower() in blob:
            score += 8
    budget = prefs.get("budget_max") or prefs.get("budget")
    tiers = {"low": 1, "medium": 2, "high": 3}
    if budget:
        wanted = "low" if budget < 800 else "medium" if budget < 2500 else "high"
        score += 12 - abs(tiers[place["budget_tier"]] - tiers[wanted]) * 6
    return max(1, min(99, score))


def local_recommendations(prefs: dict) -> dict:
    ranked = []
    for place in dest_mod.CATALOG:
        ranked.append(
            {
                "id": place["id"],
                "name": place["name"],
                "country": place["country"],
                "region": place["region"],
                "summary": place["summary"],
                "vibes": place["vibes"],
                "score": score_place(place, prefs),
                "reason": _reason(place, prefs),
                "category": "destination",
            }
        )
    ranked.sort(key=lambda item: item["score"], reverse=True)
    top = ranked[:5]
    dining, activities = [], []
    place = dest_mod.find_place(top[0]["name"], top[0]["id"]) if top else None
    if place:
        for stop in place["activities"]:
            item = {
                "id": f"{place['id']}-{stop['title'][:12]}",
                "name": stop["title"],
                "country": place["country"],
                "summary": stop.get("description") or "",
                "reason": f"Fits {stop['vibe']} / {stop['category']}",
                "score": 80,
                "category": stop["category"],
                "estimated_cost": stop.get("estimated_cost"),
                "vibes": [stop.get("vibe") or ""],
            }
            if stop["category"] == "food":
                dining.append(item)
            else:
                activities.append(item)
    return {"items": top, "dining": dining[:4], "activities": activities[:6]}


def _reason(place: dict, prefs: dict) -> str:
    vibe = enum_text(prefs.get("vibe") or prefs.get("travel_style"))
    bits = []
    if vibe and vibe in place["vibes"]:
        bits.append(f"matches your {vibe} style")
    if prefs.get("travelers", 1) > 2 and "family" in place["vibes"]:
        bits.append("works for a group")
    return " · ".join(bits) or place["summary"]


async def recommend(prefs: dict) -> dict:
    prompt = build_recommendation_prompt(prefs)
    try:
        parsed = await complete_json(prompt)
        if parsed and parsed.get("destinations"):
            items = []
            for row in parsed["destinations"]:
                known = dest_mod.find_place(row.get("name", ""), row.get("id"))
                items.append(
                    {
                        "id": (known or {}).get("id") or row.get("id") or row.get("name", "").lower(),
                        "name": (known or {}).get("name") or row.get("name"),
                        "country": (known or {}).get("country") or "",
                        "region": (known or {}).get("region") or "",
                        "summary": (known or {}).get("summary") or row.get("reason", ""),
                        "reason": row.get("reason") or "",
                        "score": row.get("score") or (score_place(known, prefs) if known else 70),
                        "vibes": (known or {}).get("vibes") or [],
                        "category": "destination",
                    }
                )
            provider = available_provider()
            return {
                "engine": provider.name if provider else "llm",
                "prompt": prompt,
                "items": items,
                "dining": parsed.get("dining") or [],
                "activities": parsed.get("activities") or [],
            }
    except Exception:
        pass
    local = local_recommendations(prefs)
    return {"engine": "rules", "prompt": prompt, **local}


def _add_days(iso: str, n: int) -> str:
    from datetime import date, timedelta

    start = date.fromisoformat(str(iso))
    return (start + timedelta(days=n)).isoformat()


def _slot_times(pace: str) -> list[tuple[str, str, str]]:
    if pace == "relaxed":
        return [("morning", "10:00", "12:00"), ("evening", "18:30", "20:30")]
    if pace == "fast":
        return [
            ("morning", "08:30", "10:30"),
            ("afternoon", "11:30", "14:00"),
            ("afternoon", "15:00", "17:00"),
            ("evening", "18:30", "21:00"),
        ]
    return [("morning", "09:00", "12:00"), ("afternoon", "13:30", "16:30"), ("evening", "18:30", "21:00")]


def local_itinerary(payload: dict) -> list[dict]:
    place = dest_mod.find_place(payload["destination"], payload.get("destination_id"))
    pool = list(place["activities"]) if place else [
        {"title": f"{payload['destination']} walk", "location": "Center", "category": "walk", "vibe": payload.get("vibe"), "duration_minutes": 90, "estimated_cost": 0, "time_slot": "morning", "description": "Orientation stroll."},
        {"title": "Signature landmark", "location": payload["destination"], "category": "landmark", "vibe": "culture", "duration_minutes": 120, "estimated_cost": 18, "time_slot": "afternoon", "description": "The sight you would regret missing."},
        {"title": "Neighborhood dinner", "location": payload["destination"], "category": "food", "vibe": "food", "duration_minutes": 100, "estimated_cost": 28, "time_slot": "evening", "description": "A meal that respects dietary notes."},
    ]
    interests = [str(i).lower() for i in (payload.get("interests") or [])]
    vibe = enum_text(payload.get("vibe") or payload.get("travel_style") or "culture")
    dietary = payload.get("dietary")
    mobility = payload.get("mobility")

    def rank(stop: dict) -> int:
        score = 1
        if stop.get("vibe") == vibe:
            score += 5
        if any(i in (stop.get("category") or "") or i in (stop.get("title") or "").lower() for i in interests):
            score += 3
        if mobility and "hike" in (stop.get("title") or "").lower():
            score -= 4
        return score

    pool.sort(key=rank, reverse=True)
    days_n = _days(payload["start_date"], payload["end_date"])
    slots = _slot_times(str(payload.get("pace") or "moderate"))
    plan = []
    for i in range(days_n):
        activities = []
        for idx, (slot, start, end) in enumerate(slots):
            stop = pool[(i + idx) % len(pool)]
            desc = stop.get("description") or ""
            if dietary and stop.get("category") == "food":
                desc = f"{desc} Dietary note: {dietary}."
            if mobility:
                desc = f"{desc} Mobility: keep transfers gentle ({mobility})."
            activities.append(
                {
                    "time_slot": slot,
                    "start_time": start,
                    "end_time": end,
                    "title": stop["title"],
                    "description": desc.strip(),
                    "location": stop.get("location"),
                    "category": stop.get("category"),
                    "vibe": stop.get("vibe"),
                    "estimated_cost": stop.get("estimated_cost") or 0,
                    "duration_minutes": stop.get("duration_minutes"),
                    "travel_minutes": 12 if idx else 0,
                    "sort_order": idx,
                }
            )
        theme = f"{vibe.title()} day {i + 1}"
        plan.append(
            {
                "day_number": i + 1,
                "date": _add_days(str(payload["start_date"]), i),
                "theme": theme,
                "summary": f"Personalized {vibe} pacing for {payload.get('travelers') or 1} traveler(s) in {payload['destination']}.",
                "activities": activities,
            }
        )
    place = dest_mod.find_place(payload["destination"], payload.get("destination_id"))
    return add_logistics(optimize_plan(plan, str(payload.get("pace") or "moderate"), place), payload, place)


def add_logistics(plan: list[dict], payload: dict, place: dict | None) -> list[dict]:
    vibe = enum_text(payload.get("vibe") or payload.get("travel_style") or "culture")
    travelers = int(payload.get("travelers") or 1)
    city = (place or {}).get("name") or payload.get("destination") or "the city"
    if vibe in {"luxury", "romance"}:
        stay = {"title": f"Boutique stay in {city}", "estimated_cost": 180 * max(1, travelers // 2), "description": "Scenic room, walkable to evening plans."}
    elif vibe in {"budget", "adventure"} or (payload.get("budget") and float(payload.get("budget") or 0) < 800):
        stay = {"title": f"Guesthouse / hostel area in {city}", "estimated_cost": 35 * travelers, "description": "Affordable base near transit."}
    elif travelers >= 3:
        stay = {"title": f"Shared apartment in {city}", "estimated_cost": 90 + 20 * travelers, "description": "Group-friendly kitchen and common space."}
    else:
        stay = {"title": f"Well-located mid-range hotel in {city}", "estimated_cost": 95, "description": "Central stay to cut transfer time."}
    transport_mode = "metro / local transit" if vibe != "luxury" else "taxi or private transfer"
    out = []
    for index, day in enumerate(plan):
        acts = list(day.get("activities") or [])
        if index == 0:
            acts.insert(
                0,
                {
                    "time_slot": "morning",
                    "start_time": "08:30",
                    "end_time": "09:15",
                    "title": stay["title"],
                    "description": stay["description"],
                    "location": city,
                    "category": "stay",
                    "vibe": vibe,
                    "estimated_cost": stay["estimated_cost"],
                    "duration_minutes": 45,
                    "travel_minutes": 0,
                    "sort_order": 0,
                },
            )
        acts.append(
            {
                "time_slot": "evening" if index < len(plan) - 1 else "evening",
                "start_time": "21:30" if index < len(plan) - 1 else "16:30",
                "title": f"Local {transport_mode}",
                "description": "Short hop between clustered stops to avoid backtracking.",
                "location": city,
                "category": "transport",
                "vibe": vibe,
                "estimated_cost": 8 if vibe != "luxury" else 28,
                "duration_minutes": 25,
                "travel_minutes": 10,
                "sort_order": 99,
            }
        )
        summary = day.get("summary") or ""
        extra = f" Stay: {stay['title']}. Group size {travelers}."
        out.append({**day, "summary": (summary + extra).strip(), "activities": acts})
    return out


async def generate_itinerary(payload: dict) -> tuple[list[dict], str, str]:
    prompt = build_itinerary_prompt(payload)
    place = dest_mod.find_place(payload.get("destination"), payload.get("destination_id"))
    pace = str(payload.get("pace") or "moderate")
    try:
        parsed = await complete_json(prompt)
        if parsed and parsed.get("days"):
            provider = available_provider()
            days = add_logistics(optimize_plan(parsed["days"], pace, place), payload, place)
            return days, prompt, provider.name if provider else "llm"
    except Exception:
        pass
    return local_itinerary(payload), prompt, "rules"
