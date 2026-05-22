from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid
import enum

class Categorie(str, enum.Enum):
    ANALYSES_TENDANCES = "Analyses & tendances"
    EVENEMENTS = "Évènements"
    ETUDES = "Études"

class ActualiteBase(BaseModel):
    image: str| None = None
    titre: str
    description: str
    categorie: Categorie

class ActualiteCreate(ActualiteBase):
    sources: list[str]

class ActualiteUpdate(BaseModel):
    image: str | None = None
    titre: str | None = None
    description: str| None = None
    categorie: Categorie | None = None
    sources: list[str] | None = None

class ActualitePublic(ActualiteBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    sources: list[str]

    model_config = ConfigDict(from_attributes=True)
