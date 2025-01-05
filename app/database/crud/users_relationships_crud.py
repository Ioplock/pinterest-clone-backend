from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import UsersRelationship, RelationshipType, User
from ...fastapi.schemas import pin_tags_schemas as schemas

# TODO: add CRUD methods