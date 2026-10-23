from fastapi import APIRouter, Depends, HTTPException, status

from ..store import repo
from ..schemas import MeResponse, TokenResponse, UserLogin, UserOut, UserRegister
from ..security import create_token, get_current_user, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(body: UserRegister):
    if repo.find_user_by_email(body.email.lower()):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = repo.create_user(body.name.strip(), body.email.lower(), hash_password(body.password))
    return TokenResponse(user=UserOut(**user), token=create_token(user))


@router.post("/login", response_model=TokenResponse)
def login(body: UserLogin):
    user = repo.find_user_by_email(body.email.lower())
    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    safe = {"id": user["id"], "name": user["name"], "email": user["email"], "created_at": user["created_at"]}
    return TokenResponse(user=UserOut(**safe), token=create_token(safe))


@router.get("/me", response_model=MeResponse)
def me(current=Depends(get_current_user)):
    user = repo.find_user_by_id(current["id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return MeResponse(user=UserOut(**user), preferences=repo.get_preferences(current["id"]))
