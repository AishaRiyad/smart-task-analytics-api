from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy import text

from app.api.routes import analytics, auth, external, tasks
from app.core.middleware import add_process_time_header
from app.db.database import Base, engine
from app.db import models
from app.core.profiler import ProfilerMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Smart Task & Analytics API",
    lifespan=lifespan
)

app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(ProfilerMiddleware)

app.middleware("http")(add_process_time_header)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(analytics.router)
app.include_router(external.router)


@app.get("/")
def root():
    return {"message": "Smart Task & Analytics API is running"}


@app.get("/health/db")
def check_database():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}