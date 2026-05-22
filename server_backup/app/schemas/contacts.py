from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
import uuid

class ContactBase(BaseModel):
    nom: str
    email: str # Could use EmailStr if email-validator is installed
    telephone: str
    objet: str
    message: str

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    nom: str | None = None
    email: str | None = None
    telephone: str | None = None
    objet: str | None = None
    message: str | None = None

class ContactPublic(ContactBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ContactMailRequest(BaseModel):
    name: str
    email: str
    subject: str | None = None
    message: str
