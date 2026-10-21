from fastapi import APIRouter, Depends

from ..store import repo
from ..schemas import PreferenceIn, RecommendationResponse
from ..security import get_current_user
from ..services.ai_engine import recommend

router = APIRouter(tags=["preferences"])


@router.get("/preferences")
def get_preferences(current=Depends(get_current_user)):
    return repo.get_preferences(current["id"]) or {}


@router.put("/preferences")
def update_preferences(body: PreferenceIn, current=Depends(get_current_user)):
    return repo.upsert_preferences(current["id"], body.model_dump(mode="json"))


@router.post("/recommendations", response_model=RecommendationResponse)
async def recommendations(body: PreferenceIn | None = None, current=Depends(get_current_user)):
    prefs = repo.get_preferences(current["id"]) or {}
    if body:
        prefs = {**prefs, **body.model_dump(mode="json")}
    result = await recommend(prefs)
    repo.log_recommendation(current["id"], result["prompt"], result["items"])
    return result
