from datetime import datetime, timedelta, timezone
from typing import Optional
import secrets

from jose import JWTError, jwt

import bcrypt

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from ..utils.jwt_utils import decode_access_token
from ..fastapi.schemas.users_schemas import TokenData
from ..database.database import get_db
from ..database.crud.users_crud import crud_user

# Secret key to encode JWT tokens
SECRET_KEY = secrets.token_hex(16)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = decode_access_token(token)
    if token_data is None or token_data.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await crud_user.get_user(db, user_id=token_data.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hashed version."""
    encoded_password = plain_password.encode('utf-8')
    return bcrypt.checkpw(encoded_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    encoded_password = password.encode('utf-8')
    return bcrypt.hashpw(encoded_password, bcrypt.gensalt())

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default to 15 minutes if no duration specified
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[TokenData]:
    """Decode a JWT token and return the token data."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        return TokenData(user_id=user_id)
    except JWTError as e:
        return None
