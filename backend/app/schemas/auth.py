"""Auth request/response schemas."""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    message: str = "Успешный вход"
    role: str


class RefreshResponse(BaseModel):
    message: str = "Токен обновлён"


class MeResponse(BaseModel):
    email: str
    role: str
