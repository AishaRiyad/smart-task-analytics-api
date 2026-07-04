def test_create_task(client):
    response = client.post("/tasks/", json={
        "title": "Test task",
        "description": "Testing create task",
        "completed": False,
        "completion_time": None
    })

    assert response.status_code == 201
    assert response.json()["title"] == "Test task"


def test_get_tasks(client):
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_task_not_found(client):
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_search_tasks(client):
    response = client.get("/tasks/search/?keyword=Test")

    assert response.status_code == 200
    assert isinstance(response.json(), list)