from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid

class ProduitBase(BaseModel):
    image: str | None = None
    nom: str
    description: str
    accroche: str
    avantages: list[str]

class ProduitCreate(ProduitBase):
    pass

class ProduitUpdate(BaseModel):
    image: str | None = None
    nom: str | None = None
    description: str | None = None
    accroche: str | None = None
    avantages: list[str] | None = None

class ProduitPublic(ProduitBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
