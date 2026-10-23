from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..security import get_current_user
from ..store import repo
from ..services.templates import get_template, list_templates, next_start, trip_payload

router = APIRouter(prefix="/templates", tags=["templates"])


class CloneBody(BaseModel):
    start_date: date | None = None
    title: str | None = None


@router.get("")
def templates():
    return list_templates()


@router.get("/{template_id}")
def template_detail(template_id: str):
    item = get_template(template_id)
    if not item:
        raise HTTPException(status_code=404, detail="Template not found")
    return item


@router.post("/{template_id}/clone", status_code=status.HTTP_201_CREATED)
def clone_template(template_id: str, body: CloneBody, current=Depends(get_current_user)):
    item = get_template(template_id)
    if not item:
        raise HTTPException(status_code=404, detail="Template not found")
    start = body.start_date or next_start()
    payload = trip_payload(item, start, body.title)
    plan = payload.pop("plan")
    trip = repo.create_trip(current["id"], payload, plan)
    return trip
