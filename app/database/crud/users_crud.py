from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user_model import User
from ...fastapi.schemas import users_schemas as schemas
from ...utils.auth import get_password_hash, verify_password

class CRUDUser:
    # READ
    async def get_user(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_users(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_user_by_username(self, db: AsyncSession, username: str):
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    # CREATE
    async def create_user(self, db: AsyncSession, user: schemas.UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = User(name=user.username, email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    # UPDATE
    async def update_user(self, db: AsyncSession, db_user: User, updates: schemas.UserUpdate):
        if updates.username is not None:
            db_user.username = updates.username
        if updates.email is not None:
            db_user.email = updates.email
        if updates.password is not None:
            db_user.hashed_password = get_password_hash(updates.password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    # DELETE
    async def delete_user(self, db: AsyncSession, db_user: User):
        await db.delete(db_user)
        await db.commit()

    # UTIL
    async def authenticate_user(self, db: AsyncSession, email: str, password: str):
        user = await self.get_user_by_email(db, email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

crud_user = CRUDUser()
