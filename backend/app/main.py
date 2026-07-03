from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes import analytics, tasks
from app.core.middleware import add_process_time_header
from app.db.database import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Task & Analytics API")

app.middleware("http")(add_process_time_header)

app.include_router(tasks.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "Smart Task & Analytics API is running"}


@app.get("/health/db")
def check_database():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}