from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy import text

from app.api.routes import analytics, auth, external, tasks
from app.core.middleware import add_process_time_header
from app.db import models
from app.db.database import Base, engine
from app.services.cache_service import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await close_redis()
    await engine.dispose()


app = FastAPI(
    title="Smart Task & Analytics API",
    lifespan=lifespan,
)

app.add_middleware(
    GZipMiddleware,
    minimum_size=500,
)

app.middleware("http")(add_process_time_header)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(analytics.router)
app.include_router(external.router)


@app.get("/")
async def root():
    return {"message": "Smart Task & Analytics API is running"}


@app.get("/health/db")
async def check_database():
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    return {"database": "connected"}