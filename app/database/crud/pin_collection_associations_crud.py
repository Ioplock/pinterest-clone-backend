from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Pin, PinCollection, PinCollectionAssociation

class CRUDPinCollectionAssociation:
    # READ
    async def get_collection_pins(self, db: AsyncSession, collection_id: int):
        result = await db.execute(select(PinCollectionAssociation).where(PinCollectionAssociation.collection_id == collection_id))
        return result.scalars().all()

crud_pin = CRUDPinCollectionAssociation()
