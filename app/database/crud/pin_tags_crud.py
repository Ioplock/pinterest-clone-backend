from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import PinTag, Pin
from ...fastapi.schemas import pin_tags_schemas as schemas

class CRUDPinTag:
    # READ
    async def get_pin_tag(self, db: AsyncSession, pin_tag_id: int):
        result = await db.execute(select(PinTag).where(PinTag.id == pin_tag_id))
        return result.scalars().first()

    async def get_pin_tags(self, db: AsyncSession):
        result = await db.execute(select(PinTag))
        return result.scalars().all()
    
    # CREATE
    async def create_pin_tag(self, db: AsyncSession, pin_tag: schemas.PinTagCreate):
        db_pin_tag = PinTag(name=pin_tag.name)
        db.add(db_pin_tag)
        await db.commit()
        await db.refresh(db_pin_tag)
        return db_pin_tag
    
    # UPDATE
    async def update_pin_tag(self, db: AsyncSession, db_pin_tag: PinTag, updates: schemas.PinTagUpdate):
        if updates.name is not None:
            db_pin_tag.name = updates.name
        db.add(db_pin_tag)
        await db.commit()
        await db.refresh(db_pin_tag)
        return db_pin_tag
    
    # DELETE
    async def delete_pin_tag(self, db: AsyncSession, db_pin_tag: PinTag):
        await db.delete(db_pin_tag)
        await db.commit(db_pin_tag)

crud_pin = CRUDPinTag()
