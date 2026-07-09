def test_create_comment_for_task(client, auth_headers):
    task_response = client.post("/tasks/", json={
        "title": "Task with comment",
        "description": "Testing comments",
        "completed": False,
        "completion_time": None
    }, headers=auth_headers)

    task_id = task_response.json()["id"]

    comment_response = client.post(
        f"/comments/?task_id={task_id}",
        json={"content": "This is a test comment"},
        headers=auth_headers
    )

    assert comment_response.status_code == 201
    assert comment_response.json()["content"] == "This is a test comment"
    assert comment_response.json()["task_id"] == task_id


def test_get_task_comments(client, auth_headers):
    task_response = client.post("/tasks/", json={
        "title": "Task comments list",
        "description": "Testing get comments",
        "completed": False,
        "completion_time": None
    }, headers=auth_headers)

    task_id = task_response.json()["id"]

    client.post(
        f"/comments/?task_id={task_id}",
        json={"content": "First comment"},
        headers=auth_headers
    )

    response = client.get(f"/comments/{task_id}", headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_delete_comment(client, auth_headers):
    task_response = client.post("/tasks/", json={
        "title": "Delete comment task",
        "description": "Testing delete comment",
        "completed": False,
        "completion_time": None
    }, headers=auth_headers)

    task_id = task_response.json()["id"]

    comment_response = client.post(
        f"/comments/?task_id={task_id}",
        json={"content": "Comment to delete"},
        headers=auth_headers
    )

    comment_id = comment_response.json()["id"]

    delete_response = client.delete(
        f"/comments/{comment_id}",
        headers=auth_headers
    )

    assert delete_response.status_code == 204