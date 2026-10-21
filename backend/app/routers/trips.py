from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from pydantic import BaseModel, Field

from ..config import CLIENT_ORIGIN
from ..store import repo
from ..schemas import ActivityCreate, TripCreate, TripOut, TripUpdate, enum_text
from ..security import get_current_user
from ..services.ai_engine import generate_itinerary
from ..services.prompt_builder import build_itinerary_prompt


class RefineBody(BaseModel):
    feedback: str = Field(..., min_length=3, max_length=800)
    vibe: str | None = None
    day_number: int | None = None

router = APIRouter(prefix="/trips", tags=["trips"])


def _payload(body: TripCreate) -> dict:
    data = body.model_dump(mode="json")
    data["start_date"] = str(body.start_date)
    data["end_date"] = str(body.end_date)
    data["vibe"] = enum_text(body.vibe or body.travel_style)
    data["travel_style"] = enum_text(body.travel_style)
    data["pace"] = enum_text(body.pace)
    return data


@router.get("", response_model=list[TripOut])
def list_trips(current=Depends(get_current_user)):
    trips = repo.list_trips(current["id"])
    return [TripOut(**{**t, "days": []}) for t in trips]


@router.post("", response_model=TripOut, status_code=status.HTTP_201_CREATED)
async def create_trip(body: TripCreate, current=Depends(get_current_user)):
    payload = _payload(body)
    prefs = repo.get_preferences(current["id"]) or {}
    payload.setdefault("dietary", prefs.get("dietary"))
    payload.setdefault("mobility", prefs.get("mobility"))
    if not payload.get("interests"):
        payload["interests"] = prefs.get("interests") or []
    plan, prompt, _engine = await generate_itinerary(payload)
    trip = repo.create_trip(current["id"], payload, plan)
    repo.log_recommendation(current["id"], prompt, {"trip_id": trip["id"]})
    return trip


@router.get("/{trip_id}", response_model=TripOut)
def get_trip(trip_id: str, current=Depends(get_current_user)):
    trip = repo.get_trip(current["id"], trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.put("/{trip_id}", response_model=TripOut)
def update_trip(trip_id: str, body: TripUpdate, current=Depends(get_current_user)):
    trip = repo.update_trip(current["id"], trip_id, body.model_dump(exclude_none=True))
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.delete("/{trip_id}", status_code=204)
def delete_trip(trip_id: str, current=Depends(get_current_user)):
    if not repo.delete_trip(current["id"], trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")
    return Response(status_code=204)


@router.post("/{trip_id}/generate", response_model=TripOut)
@router.post("/{trip_id}/regenerate", response_model=TripOut)
async def generate(trip_id: str, current=Depends(get_current_user)):
    trip = repo.get_trip(current["id"], trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    trip["previous_plan"] = trip.get("days")
    plan, prompt, _engine = await generate_itinerary(trip)
    updated = repo.replace_plan(current["id"], trip_id, plan)
    repo.log_recommendation(current["id"], prompt, {"trip_id": trip_id})
    return updated


@router.post("/{trip_id}/refine", response_model=TripOut)
async def refine(trip_id: str, body: RefineBody, current=Depends(get_current_user)):
    trip = repo.get_trip(current["id"], trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    trip["previous_plan"] = trip.get("days")
    note = body.feedback
    if body.day_number:
        note = f"Regenerate only day {body.day_number}. Keep other days. {body.feedback}"
    trip["feedback"] = note
    if body.vibe:
        trip["vibe"] = body.vibe
        trip["travel_style"] = body.vibe
    plan, prompt, _engine = await generate_itinerary(trip)
    updated = repo.replace_plan(current["id"], trip_id, plan)
    repo.log_recommendation(current["id"], prompt, {"trip_id": trip_id, "feedback": body.feedback})
    return updated


@router.post("/{trip_id}/share")
def share_trip(trip_id: str, current=Depends(get_current_user)):
    trip = repo.enable_share(current["id"], trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    token = trip["share_token"]
    return {"share_token": token, "url": f"{CLIENT_ORIGIN}/share/{token}"}


@router.get("/{trip_id}/prompt")
def trip_prompt(trip_id: str, current=Depends(get_current_user)):
    trip = repo.get_trip(current["id"], trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return {"prompt": build_itinerary_prompt(trip)}


@router.get("/{trip_id}/export")
def export_trip(trip_id: str, format: str = Query("json"), current=Depends(get_current_user)):
    trip = repo.get_trip(current["id"], trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    fmt = format.lower()
    if fmt in {"md", "markdown"}:
        lines = [f"# {trip['title']}", "", f"{trip['destination']} · {trip['start_date']} → {trip['end_date']}", ""]
        for day in trip["days"]:
            lines.append(f"## Day {day['day_number']} — {day.get('theme')}")
            for act in day["activities"]:
                lines.append(f"- **{act.get('start_time') or act['time_slot']}** {act['title']} ({act.get('location') or '—'})")
            lines.append("")
        return Response("\n".join(lines), media_type="text/markdown")
    if fmt == "ics":
        chunks = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Waypoint//Itinerary//EN"]
        for day in trip["days"]:
            for act in day["activities"]:
                stamp = str(day.get("date") or trip["start_date"]).replace("-", "")
                hhmm = (act.get("start_time") or "09:00").replace(":", "")
                chunks += [
                    "BEGIN:VEVENT",
                    f"DTSTART:{stamp}T{hhmm}00",
                    f"SUMMARY:{act['title']}",
                    f"LOCATION:{act.get('location') or trip['destination']}",
                    "END:VEVENT",
                ]
        chunks.append("END:VCALENDAR")
        return Response("\r\n".join(chunks), media_type="text/calendar")
    return trip


@router.post("/{trip_id}/days/{day_id}/activities", status_code=201)
def add_activity(trip_id: str, day_id: str, body: ActivityCreate, current=Depends(get_current_user)):
    result = repo.add_activity(current["id"], trip_id, day_id, body.model_dump())
    if result is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    if result is False:
        raise HTTPException(status_code=404, detail="Day not found")
    return result


@router.delete("/{trip_id}/activities/{activity_id}", status_code=204)
def remove_activity(trip_id: str, activity_id: str, current=Depends(get_current_user)):
    if not repo.delete_activity(current["id"], trip_id, activity_id):
        raise HTTPException(status_code=404, detail="Activity not found")
    return Response(status_code=204)
