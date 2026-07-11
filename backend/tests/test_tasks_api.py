async def test_create_task(client, auth_headers):
    response = await client.post(
        "/tasks/",
        json={
            "title": "Test task",
            "description": "Testing create task",
            "completed": False,
            "completion_time": None,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test task"


async def test_get_tasks(client, auth_headers):
    response = await client.get(
        "/tasks/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_task_not_found(client, auth_headers):
    response = await client.get(
        "/tasks/999999",
        headers=auth_headers,
    )

    assert response.status_code == 404


async def test_search_tasks(client, auth_headers):
    response = await client.get(
        "/tasks/search/?keyword=Test",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_unauthenticated_tasks_are_rejected(client):
    response = await client.get("/tasks/")

    assert response.status_code == 401