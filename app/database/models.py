from typing import Optional, List
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Table, Column
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

# PIN
pin_tag_association = Table(
    "pin_tag_associations",
    Base.metadata,
    Column("pin_id", ForeignKey("pins.id"), primary_key=True),
    Column("tag_id", ForeignKey("pin_tags.id"), primary_key=True)
)

class PinTag(Base):
    __tablename__ = "pin_tags"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    
    pins: Mapped[List["Pin"]] = relationship(secondary=pin_tag_association, back_populates="tags")

pin_collection_association = Table(
    "pin_collection_associations",
    Base.metadata,
    Column("pin_id", ForeignKey("pins.id"), primary_key=True),
    Column("collection_id", ForeignKey("pin_collections.id"), primary_key=True)
)

class PinCollection(Base):
    __tablename__ = "pin_collections"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    visibility_id: Mapped[int] = mapped_column(ForeignKey("visibility_types.id"), nullable=False)
    
    pins: Mapped[List["Pin"]] = relationship(secondary=pin_collection_association, back_populates="collections")
    owner: Mapped["User"] = relationship(back_populates="collections")
    visibility: Mapped["VisibilityType"] = relationship(back_populates="collections")

class FileType(Base):
    __tablename__ = "file_types"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(8))
    
    pins: Mapped[List["Pin"]] = relationship(back_populates="type")

pin_user_like = Table(
    "pin_like_associations",
    Base.metadata,
    Column("pin_id", ForeignKey("pins.id"), primary_key=True),
    Column("owner_id", ForeignKey("users.id"), primary_key=True)
)

class VisibilityType(Base):
    __tablename__ = "visibility_types"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    
    pins: Mapped[List["Pin"]] = relationship(back_populates="visibility")
    collections: Mapped[List["PinCollection"]] = relationship(back_populates="visibility")

class Pin(Base):
    __tablename__ = "pins"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    upload_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    type_id: Mapped[int] = mapped_column(ForeignKey("file_types.id"), nullable=True)
    visibility_id: Mapped[int] = mapped_column(ForeignKey("visibility_types.id"), nullable=False)
    
    owner: Mapped["User"] = relationship(back_populates="pins")
    type: Mapped["FileType"] = relationship(back_populates="pins")
    visibility: Mapped["VisibilityType"] = relationship(back_populates="pins")
    tags: Mapped[List["PinTag"]] = relationship(secondary=pin_tag_association, back_populates="pins")
    collections: Mapped[List["PinCollection"]] = relationship(secondary=pin_collection_association, back_populates="pins")
    likes: Mapped[List["User"]] = relationship(secondary=pin_user_like, back_populates="liked_pins")

class UsersRelationship(Base):
    __tablename__ = "users_relationships"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    related_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    relationship_type_id: Mapped[int] = mapped_column(ForeignKey("relationship_types.id"), nullable=False)

    user: Mapped["User"] = relationship(foreign_keys=[user_id], back_populates="relationships")
    related_user: Mapped["User"] = relationship(foreign_keys=[related_user_id], back_populates="related_relationships")
    relationship_type: Mapped["RelationshipType"] = relationship(back_populates="users")

class RelationshipType(Base):
    __tablename__ = "relationship_types"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    
    users: Mapped[List["UsersRelationship"]] = relationship(back_populates="relationship_type")

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), index=True, unique=True, nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    email: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    
    pins: Mapped["Pin"] = relationship(back_populates="owner")
    collections: Mapped["PinCollection"] = relationship(back_populates="owner")
    liked_pins: Mapped[List["Pin"]] = relationship(secondary=pin_user_like, back_populates="likes")
    relationships: Mapped[List["UsersRelationship"]] = relationship(
        foreign_keys="[UsersRelationship.user_id]", 
        back_populates="user"
    )
    related_relationships: Mapped[List["UsersRelationship"]] = relationship(
        foreign_keys="[UsersRelationship.related_user_id]", 
        back_populates="related_user"
    )
