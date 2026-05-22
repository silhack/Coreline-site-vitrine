from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime

class AdminBase(BaseModel):
    nom: str
    email: EmailStr # Ajout de l'email

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(BaseModel):
    nom: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class AdminPublic(AdminBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    nom: str # On pourrait aussi permettre l'email ici
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    nom: str | None = None
