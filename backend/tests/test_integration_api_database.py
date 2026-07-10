import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.main import app
from app.db.database import Base, get_db


@pytest.fixture(scope="module")
def postgres_container():
    with PostgresContainer("postgres:16") as postgres:
        yield postgres


@pytest.fixture(scope="module")
def test_db(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def integration_client(test_db):
    return TestClient(app)


def test_create_then_get_task_integration(integration_client, auth_headers):
    create_response = integration_client.post("/tasks/", json={
        "title": "Integration task",
        "description": "Testing API with isolated PostgreSQL container",
        "completed": False,
        "completion_time": None
    }, headers=auth_headers)

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    get_response = integration_client.get(
        f"/tasks/{task_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id
    assert get_response.json()["title"] == "Integration task"


def test_create_update_delete_task_integration(integration_client, auth_headers):
    create_response = integration_client.post("/tasks/", json={
        "title": "Full integration task",
        "description": "Testing create update delete",
        "completed": False,
        "completion_time": None
    }, headers=auth_headers)

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    update_response = integration_client.put(f"/tasks/{task_id}", json={
        "title": "Updated integration task",
        "description": "Updated description",
        "completed": True,
        "completion_time": 30
    }, headers=auth_headers)

    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True
    assert update_response.json()["completion_time"] == 30

    delete_response = integration_client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 204

    get_deleted_response = integration_client.get(
        f"/tasks/{task_id}",
        headers=auth_headers
    )

    assert get_deleted_response.status_code == 404