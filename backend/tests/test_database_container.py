from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.db.models import Task


def test_create_and_read_task_with_postgres_container():
    with PostgresContainer("postgres:16") as postgres:
        engine = create_engine(postgres.get_connection_url())
        TestingSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )

        Base.metadata.create_all(bind=engine)

        db = TestingSessionLocal()

        try:
            task = Task(
                title="Container test task",
                description="Testing real PostgreSQL container",
                completed=False,
                completion_time=None
            )

            db.add(task)
            db.commit()
            db.refresh(task)

            saved_task = db.query(Task).filter(Task.id == task.id).first()

            assert saved_task is not None
            assert saved_task.title == "Container test task"
            assert saved_task.completed is False

        finally:
            db.close()
            Base.metadata.drop_all(bind=engine)