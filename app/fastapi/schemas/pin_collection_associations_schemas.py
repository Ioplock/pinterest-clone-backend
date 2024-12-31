from pydantic import BaseModel
from typing import Optional

class PinCollectionAssociationCreate(BaseModel):
    pin_id: int
    collection_id: int

class PinCollectionAssociationUpdate(BaseModel):
    pin_id: Optional[int] = None
    collection_id: Optional[int] = None

class PinCollectionAssociationInDB(BaseModel):
    id: int
    pin_id: int
    collection_id: int

    class Config:
        from_attributes = True
