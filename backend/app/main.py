from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Task & Analytics API")


@app.get("/")
def root():
    return {"message": "Smart Task & Analytics API is running"}


@app.get("/health/db")
def check_database():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}