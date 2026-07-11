import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.database import Base
from app.db.models import Task, User


@pytest.mark.asyncio
async def test_create_and_read_task_with_postgres_container():
    with PostgresContainer("postgres:16") as postgres:
        database_url = postgres.get_connection_url().replace(
            "postgresql+psycopg2://",
            "postgresql+asyncpg://",
        )

        engine = create_async_engine(database_url)

        TestingSessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        async with TestingSessionLocal() as db:
            user = User(
                username="containeruser",
                email="container@example.com",
                hashed_password="hashed",
            )

            db.add(user)
            await db.commit()
            await db.refresh(user)

            task = Task(
                title="Container test task",
                description="Testing real PostgreSQL container",
                completed=False,
                completion_time=None,
                owner_id=user.id,
            )

            db.add(task)
            await db.commit()
            await db.refresh(task)

            result = await db.execute(
                select(Task).where(Task.id == task.id)
            )

            saved_task = result.scalar_one_or_none()

            assert saved_task is not None
            assert saved_task.title == "Container test task"
            assert saved_task.owner_id == user.id

        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)

        await engine.dispose()