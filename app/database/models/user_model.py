from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), index=True, unique=True, nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    email: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
