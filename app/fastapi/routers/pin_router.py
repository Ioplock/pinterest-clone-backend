from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..schemas import pins_schemas as schemas
from ...database.crud.pins_crud import crud_pin
from ...database.crud.file_types_crud import crud_file_type
from ...database.crud.pin_tags_crud import crud_tag
from ...database.database import get_db
from ...database import models
import json

router = APIRouter(
    prefix="/api/pins",
    tags=["pins"],
    responses={404: {"description": "Not found"}},
)

with open("app\\utils\\config.json", "r", encoding="UTF-8") as file:
    config = json.load(file)


@router.get("/", response_model=schemas.PinInDB)
async def read_pins(skip: int = config["DEFAULT_SKIP"], limit: int = config["DEFAULT_LIMIT"], db: AsyncSession = Depends(get_db)):
    pins = await crud_pin.get_pins(db, skip=skip, limit=limit)
    return pins

@router.post("/", response_model=schemas.PinInDB, status_code=status.HTTP_201_CREATED)
async def create_pin(pin: schemas.PinCreate, db: AsyncSession = Depends(get_db)):
    # if len(pin.title) > MAX_TITLE_LENGTH:
    #     raise HTTPException(status_code=422, detail="Title exceeds character limit")
    # if len(pin.description) > MAX_DESCRIPTION_LENGTH:
    #     raise HTTPException(status_code=422, detail="Description exceeds character limit")
    # db_type = await crud_file_type.get_file_type(db, pin.type)
    # if not db_type:
    #     raise HTTPException(status_code=422, detail="File is of an invalid type")
    # if len(pin.tags) > MAX_PIN_TAG_COUNT:
    #     raise HTTPException(status_code=422, detail="Tags count exceeds count limit")
    # for tag in pin.tags:
    #     if len(tag) > MAX_PIN_TAG_LENGTH:
    #         raise HTTPException(status_code=422, detail="Tag's name exceeds character limit")
    return await crud_pin.create_pin(db, pin)

@router.get("/{pin_id}", response_model=schemas.PinInDB)
async def read_pin(pin_id: int, db: AsyncSession = Depends(get_db)):
    db_pin = await crud_pin.get_pin(db, pin_id=pin_id)
    if db_pin is None:
        raise HTTPException(status_code=404, detail="Pin not found")
    return db_pin

@router.put("/{pin_id}", response_model=schemas.PinInDB)
async def update_pin(pin_id: int, updates: schemas.PinUpdate, db: AsyncSession = Depends(get_db)):
    db_pin = await crud_pin.get_pin(db, pin_id=pin_id)
    if db_pin is None:
        raise HTTPException(status_code=404, detail="Pin not found")
    return await crud_pin.update_pin(db, db_pin, updates)

@router.delete("/{pin_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pin(pin_id: int, db: AsyncSession = Depends(get_db)):
    db_pin = await crud_pin.get_pin(db, pin_id=pin_id)
    if db_pin is None:
        raise HTTPException(status_code=404, detail="Pin not found")
    await crud_pin.delete_pin(db, db_pin)
    return

# TODO: add routes for likes and comments (when they are implemented)
