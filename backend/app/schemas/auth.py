from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.tecnico


class UserOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    role: UserRole
    ativo: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
