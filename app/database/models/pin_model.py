from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base

# PIN
class Pin(Base):
    __tablename__ = "pins"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    upload_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
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
    collection: Mapped["PinCollection"] = relationship(back_populates="pin_collections.associations")
    added_to_collection_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    order_number: Mapped[int] = mapped_column(nullable=False)
