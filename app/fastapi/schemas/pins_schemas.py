from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class PinCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: int
    tags: Optional[List[int]] = None

class PinUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[int]] = None

class PinInDB(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    upload_timestamp: datetime
    type: int
    tags: Optional[List[int]] = None
    collections_association: Optional[List[int]] = None
    
    class Config:
        from_attributes = True
