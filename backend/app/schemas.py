from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class Pace(str, Enum):
    relaxed = "relaxed"
    moderate = "moderate"
    fast = "fast"


def enum_text(value) -> str:
    if value is None:
        return ""
    if hasattr(value, "value"):
        return str(value.value)
    text = str(value)
    if "." in text and text.split(".", 1)[0] in {"TravelStyle", "Pace"}:
        return text.split(".", 1)[1]
    return text


class TravelStyle(str, Enum):
    culture = "culture"
    adventure = "adventure"
    relaxation = "relaxation"
    food = "food"
    romance = "romance"
    family = "family"
    luxury = "luxury"
    nature = "nature"


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: Optional[str] = None


class TokenResponse(BaseModel):
    user: UserOut
    token: str
    token_type: str = "bearer"


class PreferenceIn(BaseModel):
    budget_min: Optional[float] = Field(default=None, ge=0)
    budget_max: Optional[float] = Field(default=None, ge=0)
    currency: str = "USD"
    vibe: TravelStyle = TravelStyle.culture
    climate: Optional[str] = None
    companions: str = "solo"
    travelers: int = Field(default=1, ge=1, le=20)
    interests: list[str] = []
    pace: Pace = Pace.moderate
    dietary: Optional[str] = None
    mobility: Optional[str] = None
    season: Optional[str] = None


class PreferenceOut(PreferenceIn):
    user_id: Optional[str] = None


class TripCreate(BaseModel):
    title: Optional[str] = None
    destination: str = Field(..., min_length=2, max_length=120)
    destination_id: Optional[str] = None
    start_date: date
    end_date: date
    budget: Optional[float] = Field(default=None, ge=0)
    travelers: int = Field(default=1, ge=1, le=20)
    companions: str = "solo"
    travel_style: TravelStyle = TravelStyle.culture
    vibe: Optional[TravelStyle] = None
    interests: list[str] = []
    dietary: Optional[str] = None
    mobility: Optional[str] = None
    pace: Pace = Pace.moderate
    notes: Optional[str] = None

    @model_validator(mode="after")
    def dates_ok(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        if not self.vibe:
            self.vibe = self.travel_style
        return self


class ActivityOut(BaseModel):
    id: Optional[str] = None
    time_slot: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    vibe: Optional[str] = None
    estimated_cost: float = 0
    duration_minutes: Optional[int] = None
    travel_minutes: int = 0
    sort_order: int = 0


class ActivityCreate(BaseModel):
    title: str = Field(..., min_length=2)
    time_slot: str = "afternoon"
    start_time: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    category: Optional[str] = None
    estimated_cost: float = 0

    @field_validator("time_slot")
    @classmethod
    def slot_ok(cls, value: str) -> str:
        allowed = {"morning", "afternoon", "evening"}
        if value not in allowed:
            raise ValueError("time_slot must be morning, afternoon, or evening")
        return value


class DayOut(BaseModel):
    id: Optional[str] = None
    day_number: int
    date: Optional[str] = None
    theme: Optional[str] = None
    summary: Optional[str] = None
    activities: list[ActivityOut] = []


class TripOut(BaseModel):
    id: str
    title: str
    destination: str
    destination_id: Optional[str] = None
    start_date: str
    end_date: str
    budget: Optional[float] = None
    travelers: Optional[int] = 1
    vibe: Optional[str] = None
    travel_style: Optional[str] = None
    companions: Optional[str] = "solo"
    interests: list[str] = []
    dietary: Optional[str] = None
    mobility: Optional[str] = None
    pace: Optional[str] = None
    notes: Optional[str] = None
    share_token: Optional[str] = None
    created_at: Optional[str] = None
    days: list[DayOut] = []


class TripUpdate(BaseModel):
    title: Optional[str] = None
    notes: Optional[str] = None
    budget: Optional[float] = None


class RecommendationItem(BaseModel):
    id: str = ""
    name: str
    country: str = ""
    region: str = ""
    summary: str = ""
    reason: str = ""
    score: float = 0
    vibes: list[str] = []
    category: str = "destination"
    estimated_cost: Optional[float] = None

    @model_validator(mode="after")
    def fill_id(self):
        if not self.id:
            self.id = self.name.lower().replace(" ", "-")
        return self


class RecommendationResponse(BaseModel):
    engine: str
    prompt: str
    items: list[RecommendationItem]
    dining: list[RecommendationItem] = []
    activities: list[RecommendationItem] = []


class MeResponse(BaseModel):
    user: UserOut
    preferences: Optional[dict] = None
