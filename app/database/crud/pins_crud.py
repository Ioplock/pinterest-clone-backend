from typing import List

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Pin, PinTag, FileType, PinCollection, PinCollectionAssociation
from ...fastapi.schemas import pins_schemas as schemas

class CRUDPin:
    # READ
    async def get_pin(self, db: AsyncSession, pin_id: int):
        result = await db.execute(select(Pin).where(Pin.id == pin_id))
        return result.scalars().first()
    
    async def get_pins(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(Pin).offset(skip).limit(limit))
        return result.scalars().all()
    
    # CREATE
    async def create_pin(self, db: AsyncSession, pin: schemas.PinCreate):
        result_db_pin_type = await db.execute(select(FileType).where(FileType.name == pin.type))
        db_pin_type = result_db_pin_type.scalars().first()
        db_pin = Pin(title=pin.title, description=pin.description, type=db_pin_type, tags=[])
        for tag in pin.tags:
            db_tag = await self.__get_or_create_tag(db, tag)
            print(type(db_tag))
            db_pin.tags.append(db_tag)
        db.add(db_pin)
        await db.commit()
        await db.refresh(db_pin)
        return db_pin
    
    # UPDATE
    async def update_pin(self, db: AsyncSession, db_pin: Pin, updates: schemas.PinUpdate):
        if updates.title is not None:
            db_pin.title = updates.title
        if updates.description is not None:
            db_pin.description = updates.description
        if updates.tags is not None:
            db_pin.tags = updates.tags
        db.add(db_pin)
        await db.commit()
        await db.refresh(db_pin)
        return db_pin

    # DELETE
    async def delete_pin(self, db: AsyncSession, db_pin: Pin):
        await db.delete(db_pin)
        await db.commit(db_pin)

    # UTIL
    async def __get_or_create_tag(self, db: AsyncSession, pin_tag_name: str):
        if pin_tag_name is None:
            return None
        result = await db.execute(select(PinTag).where(PinTag.name == pin_tag_name))
        instance = result.scalar_one_or_none()
        if instance is None:
            instance = PinTag(name=pin_tag_name)
            db.add(instance)
            await db.commit()
            await db.refresh(instance)
        return instance

crud_pin = CRUDPin()
