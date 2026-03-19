"""Authentication endpoints."""

from datetime import datetime, timezone

import bcrypt
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.admin_user import AdminUser
from app.schemas.auth import LoginRequest, LoginResponse, MeResponse, RefreshResponse
from app.security.dependencies import get_current_admin
from app.security.jwt import create_access_token, create_refresh_token, decode_token

router = APIRouter()

MAX_FAILED_ATTEMPTS = 5
LOCK_MINUTES = 15


def _verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def _set_tokens(response: Response, user: AdminUser) -> None:
    access = create_access_token(str(user.id), user.role)
    refresh = create_refresh_token(str(user.id))
    response.set_cookie("access_token", access, httponly=True, samesite="lax", max_age=900)
    response.set_cookie("refresh_token", refresh, httponly=True, samesite="lax", max_age=7 * 86400)


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(AdminUser).filter(AdminUser.email == body.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

    now = datetime.now(timezone.utc)
    if user.locked_until and user.locked_until > now:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Аккаунт временно заблокирован")

    if not _verify_password(body.password, user.password_hash):
        user.failed_attempts += 1
        if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
            from datetime import timedelta
            user.locked_until = now + timedelta(minutes=LOCK_MINUTES)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")

    user.failed_attempts = 0
    user.locked_until = None
    user.last_login = now
    db.commit()

    _set_tokens(response, user)
    return LoginResponse(role=user.role)


@router.post("/refresh", response_model=RefreshResponse)
def refresh(response: Response, refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет refresh токена")

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный refresh токен")

    user = db.query(AdminUser).filter(AdminUser.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")

    _set_tokens(response, user)
    return RefreshResponse()


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Выход выполнен"}


@router.get("/me", response_model=MeResponse)
def me(admin: AdminUser = Depends(get_current_admin)):
    return MeResponse(email=admin.email, role=admin.role)
