from datetime import datetime
import uuid
from typing import List
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, text, ARRAY
from app.database import Base

class Produit(Base):
    __tablename__ = "produits"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    image: Mapped[str | None] = mapped_column(String, nullable=True)
    nom: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    accroche: Mapped[str] = mapped_column(String)
    avantages: Mapped[List[str]] = mapped_column(ARRAY(String))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), onupdate=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"))
