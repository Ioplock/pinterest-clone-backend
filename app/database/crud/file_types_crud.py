from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Pin, FileType
from ...fastapi.schemas import file_types_schemas as schemas

class CRUDFileType:
    # READ
    async def get_file_type(self, db: AsyncSession, file_type_id: int):
        result = await db.execute(select(FileType).where(FileType.id == file_type_id))
        return result.scalars().first()
    
    async def get_file_types(self, db: AsyncSession):
        result = await db.execute(select(FileType))
        return result.scalars().all()
    
    # CREATE
    async def create_file_type(self, db: AsyncSession, file_type: schemas.FileTypeCreate):
        db_file_type = FileType(name=file_type.name)
        db.add(db_file_type)
        await db.commit()
        await db.refresh(db_file_type)
        return db_file_type
    
    # UPDATE
    async def update_file_type(self, db: AsyncSession, db_file_type: FileType, updates: schemas.FileTypeUpdate):
        if updates.name is not None:
            db_file_type.name = updates.name
        db.add(db_file_type)
        await db.commit()
        await db.refresh(db_file_type)
        return db_file_type
    
    # DELETE
    async def delete_file_type(self, db: AsyncSession, db_file_type: FileType):
        await db.delete(db_file_type)
        await db.commit(db_file_type)

crud_file_type = CRUDFileType()
