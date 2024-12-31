from pydantic import BaseModel
from typing import Optional

class PinCollectionCreate(BaseModel):
    title: str

class PinCollectionUpdate(BaseModel):
    title: Optional[str] = None

class PinCollectionInDB(BaseModel):
    id: int
    title: str
