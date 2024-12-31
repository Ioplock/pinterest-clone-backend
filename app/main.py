from fastapi import FastAPI
import uvicorn

from .database.database import engine, Base
from .database.models import User
from .database.models import Pin, FileType, PinTag, PinCollection, PinCollectionAssociation
from .fastapi.routers import auth_router, users_router

app = FastAPI(title="FastAPI Async SQLAlchemy Example")

# Include routers
app.include_router(users_router.router)
app.include_router(auth_router.router)

# Create database tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Optional: Shutdown event if needed
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

# To run with `python -m app.main`
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
