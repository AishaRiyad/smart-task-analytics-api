from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy import text

from app.api.routes import analytics, auth, export, external, tasks
from app.core.middleware import add_process_time_header
from app.db.database import Base, engine
from app.db import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Smart Task & Analytics API",
    lifespan=lifespan
)

app.add_middleware(GZipMiddleware, minimum_size=500)

app.middleware("http")(add_process_time_header)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(analytics.router)
app.include_router(external.router)
app.include_router(export.router)


@app.get("/")
def root():
    return {"message": "Smart Task & Analytics API is running"}


@app.get("/health/db")
def check_database():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}