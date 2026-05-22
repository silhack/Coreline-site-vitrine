from datetime import datetime
import uuid
import enum
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, text, ForeignKey, Table, Column, Enum
from app.database import Base

class Categorie(str, enum.Enum):
    ANALYSES_TENDANCES = "Analyses & tendances"
    EVENEMENTS = "Évènements"
    ETUDES = "Études"

# Association table for Many-to-Many relationship between Actualites and Source
actualite_source_link = Table(
    "actualite_source_link",
    Base.metadata,
    Column("actualite_id", ForeignKey("actualites.id"), primary_key=True),
    Column("source_id", ForeignKey("sources.id"), primary_key=True),
)

class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String, index=True, unique=True)
    
    actualites: Mapped[List["Actualite"]] = relationship(
        secondary=actualite_source_link, back_populates="sources"
    )

class Actualite(Base):
    __tablename__ = "actualites"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    image: Mapped[str | None] = mapped_column(String, nullable=True)
    titre: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    categorie: Mapped[Categorie] = mapped_column(Enum(Categorie))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), onupdate=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"))

    sources: Mapped[List[Source]] = relationship(
        secondary=actualite_source_link, back_populates="actualites"
    )
