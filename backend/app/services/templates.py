"""Ready-made itineraries for solo, couple, and group trips."""

from copy import deepcopy
from datetime import date, timedelta


def _act(slot, start, title, description, location, category, cost, minutes=90, travel=12, vibe="culture"):
    return {
        "time_slot": slot,
        "start_time": start,
        "title": title,
        "description": description,
        "location": location,
        "category": category,
        "vibe": vibe,
        "estimated_cost": cost,
        "duration_minutes": minutes,
        "travel_minutes": travel,
    }


TEMPLATES = [
    {
        "id": "paris-solo-weekend",
        "title": "Paris food & sights weekend",
        "destination": "Paris",
        "destination_id": "paris",
        "companions": "solo",
        "travelers": 1,
        "travel_style": "food",
        "vibe": "food",
        "pace": "moderate",
        "budget": 650,
        "interests": ["food", "museums", "history"],
        "nights": 2,
        "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1400&q=80",
        "blurb": "A tight solo weekend: Louvre morning, Latin Quarter lunch, Seine evening — walking-first and wallet-aware.",
        "highlights": ["Louvre timed visit", "Seine sunset", "Affordable bistros"],
        "days": [
            {
                "day_number": 1,
                "theme": "Right Bank classics",
                "summary": "Check in near the 1st, see headline art, then eat and walk along the river.",
                "activities": [
                    _act("morning", "09:00", "Marais guesthouse check-in", "Walkable base near Metro 1. Drop bags and start on foot.", "Le Marais", "stay", 90, 40, 0, "food"),
                    _act("morning", "10:00", "Louvre highlights", "Denon wing icons, then a short rest in the Tuileries.", "Rue de Rivoli", "attraction", 22, 150, 10, "culture"),
                    _act("afternoon", "13:00", "Latin Quarter lunch", "Classic plat du jour — skip tourist-menu streets one block in.", "5th arr.", "food", 28, 75, 15, "food"),
                    _act("afternoon", "15:00", "Île de la Cité walk", "Sainte-Chapelle exterior and bookstalls on the quai.", "Cité", "attraction", 0, 80, 8, "culture"),
                    _act("evening", "18:30", "Seine sunset cruise", "Monuments from the water without a long dinner booking.", "Pont Neuf", "attraction", 18, 75, 10, "romance"),
                    _act("evening", "20:30", "Metro home", "Short hop; avoid late taxis on a solo budget night.", "Metro 1", "transport", 2, 20, 0, "food"),
                ],
            },
            {
                "day_number": 2,
                "theme": "Montmartre & markets",
                "summary": "Hill views, a market lunch, then an early train-friendly evening.",
                "activities": [
                    _act("morning", "09:00", "Sacré-Cœur & back streets", "Arrive before tour groups; coffee on Rue des Abbesses.", "18th arr.", "attraction", 0, 120, 18, "culture"),
                    _act("afternoon", "12:30", "Marché des Enfants Rouges", "Shared tables and a cheap, excellent plate.", "Le Marais", "food", 16, 70, 15, "food"),
                    _act("afternoon", "14:30", "Centre Pompidou top floor", "City view if you skip the full museum.", "4th arr.", "attraction", 15, 90, 8, "culture"),
                    _act("evening", "18:00", "Wine bar + cheese", "One glass and a board — keep dinner light before travel.", "11th arr.", "food", 22, 80, 12, "food"),
                ],
            },
        ],
    },
    {
        "id": "bali-couple-escape",
        "title": "Ubud & coast for two",
        "destination": "Bali",
        "destination_id": "bali",
        "companions": "couple",
        "travelers": 2,
        "travel_style": "romance",
        "vibe": "romance",
        "pace": "relaxed",
        "budget": 1800,
        "interests": ["nature", "food", "beaches"],
        "nights": 3,
        "image": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1400&q=80",
        "blurb": "Slow mornings, rice terraces, a boutique stay, and a sunset temple — built for two, not a tour bus.",
        "highlights": ["Boutique stay", "Rice terraces", "Tanah Lot sunset"],
        "days": [
            {
                "day_number": 1,
                "theme": "Arrive & unwind",
                "summary": "Check into a scenic room, short spa, unhurried dinner.",
                "activities": [
                    _act("morning", "11:00", "Boutique stay in Ubud", "Pool and rice-field view; walkable to evening warungs.", "Ubud", "stay", 160, 45, 0, "romance"),
                    _act("afternoon", "15:00", "Campuhan Ridge walk", "Easy scenic path, not a hike. Golden light if you start late.", "Ubud", "attraction", 0, 90, 10, "nature"),
                    _act("evening", "19:00", "Tasting dinner for two", "Set menu, quieter room — book the earlier seating.", "Ubud Center", "food", 70, 120, 8, "romance"),
                ],
            },
            {
                "day_number": 2,
                "theme": "Terraces & temples",
                "summary": "Cool morning at Tegalalang, slow lunch, driver for the coast sunset.",
                "activities": [
                    _act("morning", "07:30", "Tegalalang rice terraces", "Go early; skip the swings if you want calm photos.", "Ubud", "attraction", 5, 120, 20, "nature"),
                    _act("afternoon", "12:00", "Farm-to-table lunch", "Long table, no rush. Share plates.", "Tegalalang", "food", 36, 90, 10, "food"),
                    _act("afternoon", "15:00", "Private transfer south", "One car for the afternoon instead of mixed vans.", "Tabanan road", "transport", 28, 90, 0, "romance"),
                    _act("evening", "17:45", "Tanah Lot sunset", "Temple on the rocks; stay for the last light.", "Tabanan", "attraction", 10, 90, 5, "romance"),
                ],
            },
            {
                "day_number": 3,
                "theme": "Coast morning",
                "summary": "Optional surf watch or beach club coffee, then a gentle last lunch.",
                "activities": [
                    _act("morning", "08:30", "Canggu beach walk", "Coffee facing the break; no lesson required.", "Canggu", "attraction", 8, 80, 25, "relaxation"),
                    _act("afternoon", "12:00", "Seafood lunch", "Share grilled fish before the airport run.", "Pererenan", "food", 32, 75, 10, "food"),
                ],
            },
        ],
    },
    {
        "id": "goa-friends-trip",
        "title": "Goa with friends",
        "destination": "Goa",
        "destination_id": "goa",
        "companions": "friends",
        "travelers": 4,
        "travel_style": "adventure",
        "vibe": "adventure",
        "pace": "moderate",
        "budget": 900,
        "interests": ["beaches", "food", "nightlife", "history"],
        "nights": 3,
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e1f1?auto=format&fit=crop&w=1400&q=80",
        "blurb": "Shared apartment, Old Goa morning, beach shack lunches, one night out — one budget, fewer group chats.",
        "highlights": ["Shared stay", "Old Goa", "Beach shacks"],
        "days": [
            {
                "day_number": 1,
                "theme": "Settle the house",
                "summary": "Check into a kitchen apartment, stock snacks, sunset at the beach.",
                "activities": [
                    _act("morning", "12:00", "Shared apartment in Panaji / Candolim", "Kitchen + common space so the group is not stuck in four hotel rooms.", "North Goa", "stay", 110, 40, 0, "adventure"),
                    _act("afternoon", "16:00", "Scooter / cab briefing", "One person drives; others ride. Keep night riding off the list.", "Candolim", "transport", 18, 40, 0, "adventure"),
                    _act("evening", "18:00", "Beach shack dinner", "Share platters; split the bill once.", "Baga / Calangute", "food", 14, 90, 15, "food"),
                ],
            },
            {
                "day_number": 2,
                "theme": "Heritage + spice",
                "summary": "Old Goa churches in the cool hours, then a spice-country lunch.",
                "activities": [
                    _act("morning", "09:00", "Old Goa basilicas", "UNESCO cluster — one cab for four, 90 minutes on site.", "Old Goa", "attraction", 0, 120, 25, "culture"),
                    _act("afternoon", "13:00", "Spice plantation lunch", "Thali and a short walk. Easy for mixed energy levels.", "Ponda", "food", 12, 100, 30, "food"),
                    _act("evening", "19:30", "Fontainhas stroll", "Latin Quarter lights and one cocktail stop — not a club crawl.", "Panaji", "attraction", 8, 80, 20, "culture"),
                ],
            },
            {
                "day_number": 3,
                "theme": "Water morning",
                "summary": "Optional boat or beach, then a late checkout buffer.",
                "activities": [
                    _act("morning", "08:30", "Dolphin / river boat", "Book one boat for the group to avoid wait chaos.", "Sinquerim", "attraction", 20, 120, 20, "adventure"),
                    _act("afternoon", "13:00", "Last shack lunch", "Keep it close to the apartment for bags.", "Candolim", "food", 12, 70, 10, "food"),
                ],
            },
        ],
    },
    {
        "id": "kyoto-culture-days",
        "title": "Kyoto temples, unhurried",
        "destination": "Kyoto",
        "destination_id": "kyoto",
        "companions": "solo",
        "travelers": 1,
        "travel_style": "culture",
        "vibe": "culture",
        "pace": "relaxed",
        "budget": 1100,
        "interests": ["history", "food", "nature"],
        "nights": 3,
        "image": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1400&q=80",
        "blurb": "Early shrines, noodle lunches, Gion at dusk — clustered so you are not crossing the city twice.",
        "highlights": ["Fushimi Inari dawn", "Gion evening", "IC card hops"],
        "days": [
            {
                "day_number": 1,
                "theme": "Higashiyama",
                "summary": "East side only: Kiyomizu, Sannenzaka, and a quiet dinner.",
                "activities": [
                    _act("morning", "10:00", "Guesthouse near Gion", "Bus-friendly base; skip a far suburban hotel.", "Gion", "stay", 70, 30, 0, "culture"),
                    _act("afternoon", "13:00", "Kiyomizu-dera", "Approach via Sannenzaka. Weekday if you can.", "Higashiyama", "attraction", 4, 120, 15, "culture"),
                    _act("evening", "18:00", "Nishiki + Gion walk", "Street snacks, then lantern streets after shops close.", "Central Kyoto", "food", 18, 100, 12, "food"),
                ],
            },
            {
                "day_number": 2,
                "theme": "Fushimi & south",
                "summary": "Torii gates at opening, then Arashiyama only if energy remains.",
                "activities": [
                    _act("morning", "07:00", "Fushimi Inari", "Go at opening. Turn around when crowds thicken.", "Fushimi", "attraction", 0, 120, 20, "culture"),
                    _act("afternoon", "12:00", "Udon lunch", "Sit-down bowl near the station.", "Fushimi", "food", 10, 45, 5, "food"),
                    _act("afternoon", "14:30", "Arashiyama grove", "Bamboo plus river path — skip the monkey park if tired.", "Arashiyama", "attraction", 0, 120, 25, "nature"),
                    _act("evening", "18:30", "Bus + IC card home", "One ride, no taxi.", "Kyoto city bus", "transport", 3, 40, 0, "culture"),
                ],
            },
        ],
    },
    {
        "id": "barcelona-food-couple",
        "title": "Barcelona bites & views",
        "destination": "Barcelona",
        "destination_id": "barcelona",
        "companions": "couple",
        "travelers": 2,
        "travel_style": "food",
        "vibe": "food",
        "pace": "moderate",
        "budget": 1400,
        "interests": ["food", "museums", "beaches"],
        "nights": 3,
        "image": "https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=1400&q=80",
        "blurb": "Gaudí morning, market lunch, beach evening — premium stays optional, walking most of the day.",
        "highlights": ["Sagrada timed entry", "La Boqueria", "Barceloneta sunset"],
        "days": [
            {
                "day_number": 1,
                "theme": "Eixample lines",
                "summary": "Sagrada first, then a long lunch, then a neighborhood wander.",
                "activities": [
                    _act("morning", "09:00", "Eixample mid-range hotel", "Near Metro L2/L5 so you skip most taxis.", "Eixample", "stay", 140, 30, 0, "food"),
                    _act("morning", "10:00", "Sagrada Família timed entry", "Book the earliest tower-free slot if you dislike queues.", "Eixample", "attraction", 26, 90, 10, "culture"),
                    _act("afternoon", "13:00", "Market lunch", "Stand-up seafood and juice — share two plates.", "La Boqueria", "food", 28, 70, 15, "food"),
                    _act("evening", "18:30", "Gothic Quarter & vermut", "Slow streets, one bar, no checklist.", "Barri Gòtic", "attraction", 14, 100, 10, "romance"),
                ],
            },
            {
                "day_number": 2,
                "theme": "Park & sea",
                "summary": "Park Güell early, then the beach for golden hour.",
                "activities": [
                    _act("morning", "08:30", "Park Güell", "Timed ticket. Leave before midday heat.", "Gràcia", "attraction", 10, 100, 20, "culture"),
                    _act("afternoon", "13:00", "Gràcia tapas", "Residential squares, better value than the Rambla.", "Gràcia", "food", 32, 80, 10, "food"),
                    _act("evening", "17:30", "Barceloneta walk", "Sunset on the sand, then a simple seafood dinner.", "Barceloneta", "attraction", 36, 120, 18, "romance"),
                ],
            },
        ],
    },
    {
        "id": "tokyo-solo-neon",
        "title": "Tokyo temples to neon",
        "destination": "Tokyo",
        "destination_id": "tokyo",
        "companions": "solo",
        "travelers": 1,
        "travel_style": "adventure",
        "vibe": "adventure",
        "pace": "fast",
        "budget": 1300,
        "interests": ["food", "culture", "nightlife"],
        "nights": 3,
        "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=1400&q=80",
        "blurb": "Asakusa dawn, Tsukiji bowls, Shibuya night — clustered days so the Yamanote does the work.",
        "highlights": ["Senso-ji early", "Tsukiji snacks", "Shibuya crossing"],
        "days": [
            {
                "day_number": 1,
                "theme": "East Tokyo",
                "summary": "Temples and market food on one side of town.",
                "activities": [
                    _act("morning", "08:30", "Asakusa hostel / hotel", "Near Senso-ji; cheap and central for day one.", "Asakusa", "stay", 55, 30, 0, "adventure"),
                    _act("morning", "09:00", "Senso-ji Temple", "Before Nakamise fills. Free.", "Asakusa", "attraction", 0, 80, 5, "culture"),
                    _act("afternoon", "11:30", "Tsukiji outer market", "Tamagoyaki and a tuna bowl. Stand, don’t linger.", "Tsukiji", "food", 22, 80, 20, "food"),
                    _act("evening", "18:30", "Izakaya counter", "Solo-friendly yakitori. One beer, then walk back.", "Asakusa", "food", 32, 90, 15, "food"),
                ],
            },
            {
                "day_number": 2,
                "theme": "West Tokyo",
                "summary": "Meiji forest, Harajuku, Shibuya night.",
                "activities": [
                    _act("morning", "09:00", "Meiji Jingu", "Forest walk into the shrine — a quiet hour.", "Shibuya", "attraction", 0, 75, 25, "culture"),
                    _act("afternoon", "12:00", "Harajuku snacks", "Takeshita-dori in and out; Omotesando for a sit-down.", "Harajuku", "food", 18, 90, 8, "food"),
                    _act("evening", "18:00", "Shibuya Crossing + rooftop", "Scramble, then a cheap observation deck.", "Shibuya", "attraction", 15, 90, 5, "adventure"),
                    _act("evening", "20:00", "Yamanote back east", "JR, not a taxi.", "JR Yamanote", "transport", 3, 30, 0, "adventure"),
                ],
            },
        ],
    },
]


def list_templates() -> list[dict]:
    out = []
    for item in TEMPLATES:
        days = item["days"]
        out.append(
            {
                "id": item["id"],
                "title": item["title"],
                "destination": item["destination"],
                "destination_id": item.get("destination_id"),
                "companions": item["companions"],
                "travelers": item["travelers"],
                "travel_style": item["travel_style"],
                "vibe": item["vibe"],
                "pace": item["pace"],
                "budget": item["budget"],
                "nights": item["nights"],
                "image": item["image"],
                "blurb": item["blurb"],
                "highlights": item["highlights"],
                "day_count": len(days),
            }
        )
    return out


def get_template(template_id: str) -> dict | None:
    for item in TEMPLATES:
        if item["id"] == template_id:
            return deepcopy(item)
    return None


def next_start(prefer_saturday: bool = True) -> date:
    today = date.today()
    if not prefer_saturday:
        return today + timedelta(days=1)
    delta = (5 - today.weekday()) % 7
    start = today + timedelta(days=delta)
    if start <= today:
        start += timedelta(days=7)
    return start


def dated_plan(template: dict, start: date) -> tuple[list[dict], date, date]:
    plan = deepcopy(template["days"])
    for index, day in enumerate(plan):
        day["date"] = (start + timedelta(days=index)).isoformat()
        day["day_number"] = index + 1
        for idx, act in enumerate(day.get("activities") or []):
            act["sort_order"] = idx
    end = start + timedelta(days=max(0, len(plan) - 1))
    return plan, start, end


def trip_payload(template: dict, start: date, title: str | None = None) -> dict:
    plan, start_d, end_d = dated_plan(template, start)
    return {
        "title": title or template["title"],
        "destination": template["destination"],
        "destination_id": template.get("destination_id"),
        "start_date": start_d.isoformat(),
        "end_date": end_d.isoformat(),
        "budget": template.get("budget"),
        "travelers": template.get("travelers") or 1,
        "companions": template.get("companions") or "solo",
        "travel_style": template.get("travel_style") or "culture",
        "vibe": template.get("vibe") or template.get("travel_style") or "culture",
        "interests": template.get("interests") or [],
        "pace": template.get("pace") or "moderate",
        "notes": f"Started from ready-made plan: {template['id']}",
        "plan": plan,
    }
