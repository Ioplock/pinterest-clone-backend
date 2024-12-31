from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

# PIN
class Pin(Base):
    __tablename__ = "pins"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    owner_id: Mapped[List[int]] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship(back_populates="pins")
    upload_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    type_id: Mapped[int] = mapped_column(ForeignKey("file_types.id"), nullable=False)
    type: Mapped["FileType"] = relationship(back_populates="file_types.pins")
    tags: Mapped[List["PinTag"]] = relationship(back_populates="pin_tags.pins")
    collections_association: Mapped[List["PinCollectionAssociation"]] = relationship(
        back_populates="pin_collection_associations.pins", cascade="all, delete, delete-orphan"
    )

class FileType(Base):
    __tablename__ = "file_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(8))
    pins: Mapped[List["Pin"]] = relationship(back_populates="type")

class PinTag(Base):
    __tablename__ = "pin_tags"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    pins: Mapped[List["Pin"]] = relationship(back_populates="tags")

# COLLECTION
class PinCollection(Base):
    __tablename__ = "pin_collections"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    pins_association: Mapped[List["Pin"]] = relationship(
        back_populates="collections", cascade="all, delete, delete-orphan"
    )

class PinCollectionAssociation(Base):
    __tablename__ = "pin_collection_associations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    pin: Mapped["Pin"] = relationship(back_populates="pins.associations")
    pin_id: Mapped[int] = mapped_column(ForeignKey("pins.id"), nullable=False)
    collection: Mapped["PinCollection"] = relationship(back_populates="pin_collections.associations")
    collection_id: Mapped[int] = mapped_column(ForeignKey("pin_collections.id"), nullable=False)
    added_to_collection_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    order_number: Mapped[int] = mapped_column(nullable=True) # TODO: Do something with this thing? Make it auto-generated..?

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), index=True, unique=True, nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    email: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    pins: Mapped["Pin"] = relationship(back_populates="owner")
