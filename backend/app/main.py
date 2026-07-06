import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.api.routes import analytics, external, tasks
from app.core.middleware import add_process_time_header
from app.db.database import Base, engine
from app.db import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    for attempt in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connected successfully.")
            break
        except OperationalError:
            print(f"Database not ready... retry {attempt + 1}/10")
            time.sleep(2)
    else:
        raise RuntimeError("Could not connect to the database.")

    yield


app = FastAPI(
    title="Smart Task & Analytics API",
    lifespan=lifespan
)

app.middleware("http")(add_process_time_header)

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