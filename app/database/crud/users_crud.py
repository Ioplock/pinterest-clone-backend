from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import user_model
from ...fastapi.schemas import users_schemas as schemas
from ...utils.auth import get_password_hash, verify_password

class CRUDUser:
    async def get_user(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(user_model.User).where(user_model.User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(select(user_model.User).where(user_model.User.email == email))
        return result.scalars().first()

    async def get_users(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(user_model.User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create_user(self, db: AsyncSession, user: schemas.UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = user_model.User(name=user.name, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def authenticate_user(self, db: AsyncSession, email: str, password: str):
        user = await self.get_user_by_email(db, email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    async def update_user(self, db: AsyncSession, db_user: user_model.User, updates: schemas.UserUpdate):
        if updates.name is not None:
            db_user.name = updates.name
        if updates.email is not None:
            db_user.email = updates.email
        if updates.password is not None:
            db_user.hashed_password = get_password_hash(updates.password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    async def delete_user(self, db: AsyncSession, db_user: user_model.User):
        await db.delete(db_user)
        await db.commit()

crud_user = CRUDUser()
