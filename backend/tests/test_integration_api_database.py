def test_create_then_get_task_integration(client):
    create_response = client.post("/tasks/", json={
        "title": "Integration task",
        "description": "Testing API with database flow",
        "completed": False,
        "completion_time": None
    })

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id
    assert get_response.json()["title"] == "Integration task"


def test_create_update_delete_task_integration(client):
    create_response = client.post("/tasks/", json={
        "title": "Full integration task",
        "description": "Testing create update delete",
        "completed": False,
        "completion_time": None
    })

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    update_response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated integration task",
        "description": "Updated description",
        "completed": True,
        "completion_time": 30
    })

    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True
    assert update_response.json()["completion_time"] == 30

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204

    get_deleted_response = client.get(f"/tasks/{task_id}")

    assert get_deleted_response.status_code == 404