from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from .database.database import engine, Base
from .database.models import User, Pin, FileType, PinTag, PinCollection, PinCollectionAssociation
from .fastapi.routers import auth_router, users_router, pin_router

app = FastAPI(title="FastAPI Async SQLAlchemy Example")

# Include routers
app.include_router(users_router.router)
app.include_router(pin_router.router)
app.include_router(auth_router.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )

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
