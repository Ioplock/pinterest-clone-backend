from pydantic import BaseModel
from typing import Optional

class PinTagCreate(BaseModel):
    name: str

class PinTagUpdate(BaseModel):
    name: Optional[str] = None

class PinTagInDB(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
