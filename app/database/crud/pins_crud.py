from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Pin, PinTag, FileType, PinCollection, PinCollectionAssociation
from ...fastapi.schemas import pins_schemas as schemas

class CRUDPin:
    # READ
    async def get_pin(self, db: AsyncSession, pin_id: int):
        result = await db.execute(select(Pin).where(Pin.id == pin_id))
        return result.scalars().first()
    
    async def get_pins(self, db: AsyncSession):
        result = await db.execute(select(Pin))
        return result.scalars().all()
    
    # CREATE
    async def create_pin(self, db: AsyncSession, pin: schemas.PinCreate):
        db_pin = Pin(title=pin.title, description=pin.description, type=pin.type, tags=pin.tags)
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

crud_pin = CRUDPin()
