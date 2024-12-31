from pydantic import BaseModel
from typing import Optional

class FileTypeCreate(BaseModel):
    name: str

class FileTypeUpdate(BaseModel):
    name: Optional[str] = None

class FileTypeInDB(BaseModel):
    id: int
    name: str
