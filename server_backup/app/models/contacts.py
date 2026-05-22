from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, text
from app.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nom: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, index=True)
    telephone: Mapped[str] = mapped_column(String, index=True)
    objet: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), onupdate=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"))