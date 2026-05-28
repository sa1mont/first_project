from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole

class UserCreate(BaseModel):
    """Схема для входящих данных при регистрации."""
    email: EmailStr
    password: str = Field(..., min_length=6, description="Пароль должен быть не менее 6 символов")

class UserOut(BaseModel):
    """Схема для безопасного ответа клиенту (без пароля)."""
    id: int
    email: EmailStr
    role: UserRole
    is_active: bool

    model_config = {"from_attributes": True}

class Token(BaseModel):
    """Схема для ответа с JWT токеном."""
    access_token: str
    token_type: str = "bearer"