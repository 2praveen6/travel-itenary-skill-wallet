"""Prompt-engineering layer between FastAPI and the AI itinerary engine."""

from datetime import date

PACE_INSTRUCTIONS = {
    "relaxed": "Keep 2 high-quality stops per day, long meals, and buffer time. No back-to-back museums.",
    "slow": "Keep 2 high-quality stops per day, long meals, and buffer time. No back-to-back museums.",
    "moderate": "Plan 3 slots (morning, afternoon, evening) with realistic walking gaps.",
    "fast": "Pack 4 focused stops, still clustered geographically. Mention transfer time explicitly.",
    "packed": "Pack 4 focused stops, still clustered geographically. Mention transfer time explicitly.",
}

VIBE_INSTRUCTIONS = {
    "culture": "Prioritize museums, heritage, and neighborhood walks.",
    "adventure": "Prioritize active outdoor stops and viewpoint hikes.",
    "relaxation": "Prioritize parks, spas, beaches, and unhurried meals.",
    "food": "Build the day around markets, cafés, and a destination dinner.",
    "romance": "Prefer scenic, quieter venues and sunset viewpoints.",
    "family": "Choose easy logistics, parks, and early dinners.",
    "luxury": "Headline sights, design-led venues, and tasting menus.",
    "nature": "Trails, water, and lookouts with short urban transfers.",
    "budget": "Favor free or low-cost stops and local eateries.",
}


def _list(values) -> str:
    if isinstance(values, list):
        return ", ".join(str(v) for v in values if v) or "general sightseeing"
    return str(values or "general sightseeing")


def _days(start: date | str, end: date | str) -> int:
    start_d = date.fromisoformat(str(start))
    end_d = date.fromisoformat(str(end))
    return max(1, (end_d - start_d).days + 1)


def build_system_role() -> str:
    return (
        "You are a senior travel designer. You never invent closed attractions, "
        "you respect dietary and mobility constraints, and you return valid JSON only."
    )


def build_recommendation_prompt(prefs: dict) -> str:
    return "\n".join(
        [
            build_system_role(),
            "Task: recommend 3-5 destinations and matching dining + activity ideas.",
            'JSON shape: {"destinations":[{"id","name","reason","score"}],"dining":[{"name","reason"}],"activities":[{"name","reason"}]}',
            f"Travel style / vibe: {prefs.get('vibe') or prefs.get('travel_style') or 'culture'}",
            f"Climate: {prefs.get('climate') or 'any'}",
            f"Group: {prefs.get('companions') or 'solo'} · travelers: {prefs.get('travelers') or 1}",
            f"Pace: {prefs.get('pace') or 'moderate'} — {PACE_INSTRUCTIONS.get(str(prefs.get('pace') or 'moderate'), '')}",
            f"Budget range: {prefs.get('budget_min') or 0}-{prefs.get('budget_max') or 'open'} {prefs.get('currency') or 'USD'}",
            f"Interests: {_list(prefs.get('interests'))}",
            f"Dietary: {prefs.get('dietary') or 'none specified'}",
            f"Mobility: {prefs.get('mobility') or 'none specified'}",
            "Prefer catalog ids when they fit: paris, tokyo, rome, bali, goa, kyoto, barcelona, jaipur.",
        ]
    )


def build_itinerary_prompt(payload: dict) -> str:
    days = _days(payload["start_date"], payload["end_date"])
    pace = str(payload.get("pace") or "moderate")
    style = payload.get("travel_style") or payload.get("vibe") or "culture"
    lines = [
            build_system_role(),
            "Task: build a day-by-day itinerary grounded in the traveler profile.",
            'JSON shape: {"days":[{"day_number","theme","summary","activities":[{"title","time_slot","location","description","duration_minutes","estimated_cost","category"}]}]}',
            "Include stay (category stay), dining (food), attractions, and local transport (category transport) with estimated_cost.",
            f"Destination: {payload.get('destination')}",
            f"Dates: {payload.get('start_date')} to {payload.get('end_date')} ({days} days)",
            f"Travelers: {payload.get('travelers') or 1} · companions: {payload.get('companions') or 'solo'}",
            f"Travel style: {style}",
            f"Interests: {_list(payload.get('interests'))}",
            f"Budget: {payload.get('budget') or 'flexible'}",
            f"Pace: {pace}. {PACE_INSTRUCTIONS.get(pace, PACE_INSTRUCTIONS['moderate'])}",
            f"Dietary restrictions: {payload.get('dietary') or 'none'}. Every meal suggestion must respect this.",
            f"Mobility concerns: {payload.get('mobility') or 'none'}. Avoid long stair-only sites if mobility is limited.",
            f"Vibe personalization: {VIBE_INSTRUCTIONS.get(str(style), VIBE_INSTRUCTIONS['culture'])}",
            "Use morning, afternoon, evening slots. Cluster nearby places to minimize backtracking.",
            "Write like a travel expert: specific venue names, why it fits this traveler, and a short transfer note.",
        ]
    previous = payload.get("previous_plan")
    feedback = payload.get("feedback")
    if previous:
        lines.append("Previous itinerary context (preserve what still fits, change what the traveler rejected):")
        lines.append(str(previous)[:2500])
    if feedback:
        lines.append(f"Traveler refinement request: {feedback}")
    return "\n".join(lines)
