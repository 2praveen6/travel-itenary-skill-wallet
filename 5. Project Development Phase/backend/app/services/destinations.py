CATALOG = [
    {
        "id": "paris",
        "name": "Paris",
        "country": "France",
        "region": "Europe",
        "vibes": ["culture", "romance", "food", "luxury"],
        "climates": ["mild", "cool"],
        "budget_tier": "high",
        "summary": "Museums, cafés, and evening walks along the Seine.",
        "activities": [
            {"title": "Louvre highlights", "location": "Rue de Rivoli", "category": "museum", "vibe": "culture", "duration_minutes": 150, "estimated_cost": 22, "time_slot": "morning", "description": "Denon wing icons, then sculpture courts."},
            {"title": "Tuileries picnic", "location": "1st arr.", "category": "walk", "vibe": "romance", "duration_minutes": 60, "estimated_cost": 12, "time_slot": "afternoon", "description": "Garden rest between museums."},
            {"title": "Seine sunset cruise", "location": "Pont Neuf", "category": "leisure", "vibe": "romance", "duration_minutes": 75, "estimated_cost": 18, "time_slot": "evening", "description": "Monuments from the water."},
            {"title": "Latin Quarter bistro", "location": "5th arr.", "category": "food", "vibe": "food", "duration_minutes": 90, "estimated_cost": 32, "time_slot": "afternoon", "description": "Classic French lunch."},
            {"title": "Montmartre & Sacré-Cœur", "location": "18th arr.", "category": "viewpoint", "vibe": "romance", "duration_minutes": 120, "estimated_cost": 0, "time_slot": "evening", "description": "Hilltop dusk views."},
            {"title": "Eiffel Tower timed entry", "location": "Champ de Mars", "category": "landmark", "vibe": "luxury", "duration_minutes": 120, "estimated_cost": 35, "time_slot": "morning", "description": "Book a summit or second-floor slot."},
        ],
    },
    {
        "id": "tokyo",
        "name": "Tokyo",
        "country": "Japan",
        "region": "Asia",
        "vibes": ["culture", "food", "adventure"],
        "climates": ["mild", "warm"],
        "budget_tier": "high",
        "summary": "Temples at dawn, neon nights, and world-class casual food.",
        "activities": [
            {"title": "Senso-ji Temple", "location": "Asakusa", "category": "temple", "vibe": "culture", "duration_minutes": 90, "estimated_cost": 0, "time_slot": "morning", "description": "Arrive before Nakamise crowds."},
            {"title": "Tsukiji outer market", "location": "Tsukiji", "category": "food", "vibe": "food", "duration_minutes": 90, "estimated_cost": 22, "time_slot": "morning", "description": "Tamagoyaki and tuna bowls."},
            {"title": "Meiji Jingu", "location": "Shibuya", "category": "shrine", "vibe": "culture", "duration_minutes": 75, "estimated_cost": 0, "time_slot": "morning", "description": "Forest walk into the shrine."},
            {"title": "Harajuku & Omotesando", "location": "Harajuku", "category": "walk", "vibe": "adventure", "duration_minutes": 120, "estimated_cost": 20, "time_slot": "afternoon", "description": "Street snacks and design shops."},
            {"title": "Shibuya Crossing night", "location": "Shibuya", "category": "landmark", "vibe": "adventure", "duration_minutes": 90, "estimated_cost": 15, "time_slot": "evening", "description": "Neon scramble and rooftop view."},
            {"title": "Izakaya dinner", "location": "Asakusa", "category": "food", "vibe": "food", "duration_minutes": 100, "estimated_cost": 40, "time_slot": "evening", "description": "Yakitori and highballs."},
        ],
    },
    {
        "id": "rome",
        "name": "Rome",
        "country": "Italy",
        "region": "Europe",
        "vibes": ["culture", "food", "romance"],
        "climates": ["warm", "mild"],
        "budget_tier": "medium",
        "summary": "Ancient streets, trattorie, and golden-hour piazzas.",
        "activities": [
            {"title": "Colosseum & Forum", "location": "Palatine", "category": "landmark", "vibe": "culture", "duration_minutes": 180, "estimated_cost": 24, "time_slot": "morning", "description": "Timed entry, Palatine overview."},
            {"title": "Trastevere dinner", "location": "Trastevere", "category": "food", "vibe": "food", "duration_minutes": 120, "estimated_cost": 40, "time_slot": "evening", "description": "Cacio e pepe in lantern lanes."},
            {"title": "Vatican Museums", "location": "Vatican City", "category": "museum", "vibe": "culture", "duration_minutes": 180, "estimated_cost": 25, "time_slot": "morning", "description": "Earliest slot; Sistine last."},
            {"title": "Trevi & Navona evening", "location": "Centro Storico", "category": "walk", "vibe": "romance", "duration_minutes": 120, "estimated_cost": 12, "time_slot": "evening", "description": "Aperitivo and a coin toss."},
        ],
    },
    {
        "id": "bali",
        "name": "Bali",
        "country": "Indonesia",
        "region": "Asia",
        "vibes": ["relaxation", "nature", "adventure", "romance"],
        "climates": ["tropical", "warm"],
        "budget_tier": "medium",
        "summary": "Rice terraces, temples, and slow coastal evenings.",
        "activities": [
            {"title": "Tegalalang rice terraces", "location": "Ubud", "category": "nature", "vibe": "nature", "duration_minutes": 120, "estimated_cost": 5, "time_slot": "morning", "description": "Go early for cooler air."},
            {"title": "Surf lesson", "location": "Canggu", "category": "sport", "vibe": "adventure", "duration_minutes": 150, "estimated_cost": 40, "time_slot": "morning", "description": "Beginner-friendly beach break."},
            {"title": "Warung dinner", "location": "Ubud Center", "category": "food", "vibe": "food", "duration_minutes": 90, "estimated_cost": 12, "time_slot": "evening", "description": "Nasi campur and juice."},
            {"title": "Tanah Lot sunset", "location": "Tabanan", "category": "temple", "vibe": "romance", "duration_minutes": 90, "estimated_cost": 10, "time_slot": "evening", "description": "Temple on the rocks."},
        ],
    },
    {
        "id": "goa",
        "name": "Goa",
        "country": "India",
        "region": "South Asia",
        "vibes": ["relaxation", "food", "adventure", "family"],
        "climates": ["tropical", "warm"],
        "budget_tier": "low",
        "summary": "Heritage churches, beach shacks, and spice-country lunches.",
        "activities": [
            {"title": "Old Goa churches", "location": "Old Goa", "category": "heritage", "vibe": "culture", "duration_minutes": 120, "estimated_cost": 0, "time_slot": "morning", "description": "UNESCO basilicas."},
            {"title": "Fontainhas walk", "location": "Panaji", "category": "walk", "vibe": "culture", "duration_minutes": 90, "estimated_cost": 8, "time_slot": "afternoon", "description": "Portuguese lanes and cafés."},
            {"title": "Beach shack dinner", "location": "Calangute", "category": "food", "vibe": "food", "duration_minutes": 120, "estimated_cost": 20, "time_slot": "evening", "description": "Grilled catch of the day."},
            {"title": "Palolem morning", "location": "South Goa", "category": "beach", "vibe": "relaxation", "duration_minutes": 150, "estimated_cost": 0, "time_slot": "morning", "description": "Quiet swim and shade."},
        ],
    },
    {
        "id": "kyoto",
        "name": "Kyoto",
        "country": "Japan",
        "region": "Asia",
        "vibes": ["culture", "romance", "nature"],
        "climates": ["mild", "cool"],
        "budget_tier": "medium",
        "summary": "Quiet temples, gardens, and lantern-lit Gion.",
        "activities": [
            {"title": "Fushimi Inari hike", "location": "Fushimi", "category": "temple", "vibe": "adventure", "duration_minutes": 120, "estimated_cost": 0, "time_slot": "morning", "description": "Torii gates before crowds."},
            {"title": "Arashiyama bamboo", "location": "Arashiyama", "category": "nature", "vibe": "nature", "duration_minutes": 90, "estimated_cost": 0, "time_slot": "afternoon", "description": "Grove and river path."},
            {"title": "Gion evening walk", "location": "Gion", "category": "walk", "vibe": "romance", "duration_minutes": 90, "estimated_cost": 20, "time_slot": "evening", "description": "Lantern streets and tea."},
        ],
    },
    {
        "id": "barcelona",
        "name": "Barcelona",
        "country": "Spain",
        "region": "Europe",
        "vibes": ["culture", "food", "relaxation", "family"],
        "climates": ["warm", "mild"],
        "budget_tier": "medium",
        "summary": "Gaudí, tapas, and a late-night beach city.",
        "activities": [
            {"title": "Sagrada Família", "location": "Eixample", "category": "landmark", "vibe": "culture", "duration_minutes": 90, "estimated_cost": 33, "time_slot": "morning", "description": "Timed nave visit."},
            {"title": "Park Güell", "location": "Gràcia", "category": "park", "vibe": "family", "duration_minutes": 90, "estimated_cost": 10, "time_slot": "afternoon", "description": "Mosaics and city views."},
            {"title": "Tapas in El Born", "location": "El Born", "category": "food", "vibe": "food", "duration_minutes": 120, "estimated_cost": 35, "time_slot": "evening", "description": "Small plates crawl."},
            {"title": "Barceloneta beach", "location": "Barceloneta", "category": "beach", "vibe": "relaxation", "duration_minutes": 90, "estimated_cost": 0, "time_slot": "afternoon", "description": "Sea air and a slow walk."},
        ],
    },
    {
        "id": "jaipur",
        "name": "Jaipur",
        "country": "India",
        "region": "South Asia",
        "vibes": ["culture", "family", "food"],
        "climates": ["hot", "warm"],
        "budget_tier": "low",
        "summary": "Pink City forts, bazaars, and Rajasthani thalis.",
        "activities": [
            {"title": "Amber Fort", "location": "Amer", "category": "fort", "vibe": "culture", "duration_minutes": 150, "estimated_cost": 6, "time_slot": "morning", "description": "Hill fort and courtyard palaces."},
            {"title": "City Palace & bazaar", "location": "Pink City", "category": "heritage", "vibe": "family", "duration_minutes": 120, "estimated_cost": 10, "time_slot": "afternoon", "description": "Textiles and palaces."},
            {"title": "Rajasthani thali", "location": "C-Scheme", "category": "food", "vibe": "food", "duration_minutes": 90, "estimated_cost": 15, "time_slot": "evening", "description": "Regional dinner."},
        ],
    },
]


def find_place(destination: str, destination_id: str | None = None):
    key = "".join(ch for ch in (destination or "").lower() if ch.isalpha())
    for place in CATALOG:
        if destination_id and place["id"] == destination_id:
            return place
        if place["id"] == key or place["name"].lower() == (destination or "").lower():
            return place
    return None
