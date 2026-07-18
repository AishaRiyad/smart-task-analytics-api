async def test_create_then_get_task_integration(
    client,
    auth_headers,
):
    create_response = await client.post(
        "/tasks/",
        json={
            "title": "Integration task",
            "description": "Testing API with isolated PostgreSQL container",
            "completed": False,
            "completion_time": None,
        },
        headers=auth_headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    get_response = await client.get(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id
    assert get_response.json()["title"] == "Integration task"


async def test_create_update_delete_task_integration(
    client,
    auth_headers,
):
    create_response = await client.post(
        "/tasks/",
        json={
            "title": "Full integration task",
            "description": "Testing create update delete",
            "completed": False,
            "completion_time": None,
        },
        headers=auth_headers,
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    update_response = await client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated integration task",
            "description": "Updated description",
            "completed": True,
            "completion_time": 30,
        },
        headers=auth_headers,
    )

    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True
    assert update_response.json()["completion_time"] == 30

    delete_response = await client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 204

    get_deleted_response = await client.get(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert get_deleted_response.status_code == 404