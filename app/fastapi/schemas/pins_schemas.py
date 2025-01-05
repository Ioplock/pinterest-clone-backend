from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import json

from ...utils.config import config

class PinCreate(BaseModel):
    title: str = Field(max_length=config["MAX_PIN_TITLE_LENGTH"])
    description: Optional[str] = Field(default=None, max_length=config["MAX_PIN_DESCRIPTION_LENGTH"])
    owner_id: int
    visibility: str
    type: str
    tags: Optional[List[str]] = Field(default=None, max_length=config["MAX_PIN_TAGS_COUNT"])

class PinUpdate(BaseModel):
    title: Optional[str] = Field(max_length=config["MAX_PIN_TITLE_LENGTH"])
    description: Optional[str] = Field(default=None, max_length=config["MAX_PIN_DESCRIPTION_LENGTH"])
    tags: Optional[List[str]] = Field(default=None, max_length=config["MAX_PIN_TAGS_COUNT"])

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
