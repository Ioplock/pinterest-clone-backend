from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Pin, PinCollection, PinCollectionAssociation
from ...fastapi.schemas import pin_collections_schemas as schemas

class CRUDPinCollection:
    # READ
    async def get_pin_collection(self, db: AsyncSession, pin_collection_id: int):
        result = await db.execute(select(PinCollection).where(PinCollection.id == pin_collection_id))
        return result.scalars().first()

    async def get_pin_collections(self, db: AsyncSession):
        result = await db.execute(select(PinCollection))
        return result.scalars().all()
    
    # CREATE
    async def create_pin_collection(self, db: AsyncSession, pin_collection: schemas.PinCollectionCreate):
        db_pin_collection = PinCollection(title=pin_collection.title)
        db.add(db_pin_collection)
        await db.commit()
        await db.refresh(db_pin_collection)
        return db_pin_collection
    
    # UPDATE
    async def update_pin_collection(self, db: AsyncSession, db_pin_collection: PinCollection, updates: schemas.PinCollectionUpdate):
        if updates.title is not None:
            db_pin_collection.title = updates.title
        db.add(db_pin_collection)
        await db.commit()
        await db.refresh(db_pin_collection)
        return db_pin_collection
    
    async def add_pin_to_collection(self, db: AsyncSession, pin_id: int, collection_id: int):
        pin_result = await db.execute(select(Pin).where(Pin.id == pin_id))
        db_pin = pin_result.scalars().first()
        collection_result = await db.execute(select(PinCollection).where(PinCollection.id == collection_id))
        db_collection = collection_result.scalars().first()
        if db_pin is None and db_collection is None:
            return None
        db_association = PinCollectionAssociation(pin_id=db_pin.id, collection_id=db_collection.id)
        db.add(db_association)
        await db.commit()
        await db.refresh(db_association)
        return db_association
    
    # DELETE
    async def delete_pin_collection(self, db: AsyncSession, db_pin_collection: PinCollection):
        await db.delete(db_pin_collection)
        await db.commit()
    
    async def remove_pin_from_collection(self, db: AsyncSession, pin_id: int, collection_id: int):
        result = await db.execute(select(PinCollectionAssociation).where(PinCollectionAssociation.pin_id == pin_id, PinCollectionAssociation.collection_id == collection_id))
        db_association = result.scalars().first()
        if db_association is None:
            return None
        await db.delete(db_association)
        await db.commit()
        return db_association

crud_pin = CRUDPinCollection()
