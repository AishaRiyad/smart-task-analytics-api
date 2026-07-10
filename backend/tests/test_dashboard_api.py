def create_task(
    client,
    auth_headers,
    title: str,
    completed: bool,
    completion_time: int | None = None,
):
    response = client.post(
        "/tasks/",
        json={
            "title": title,
            "description": "Dashboard test task",
            "completed": completed,
            "completion_time": completion_time,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201
    return response.json()


def test_get_analytics_dashboard(client, auth_headers):
    create_task(
        client,
        auth_headers,
        title="Completed dashboard task",
        completed=True,
        completion_time=20,
    )

    create_task(
        client,
        auth_headers,
        title="Pending dashboard task",
        completed=False,
    )

    response = client.get(
        "/analytics/dashboard?days=7",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data
    assert "completion_rate" in data
    assert "tasks_created_by_day" in data
    assert "tasks_completed_by_day" in data

    assert data["summary"]["total_tasks"] >= 2
    assert data["summary"]["completed_tasks"] >= 1
    assert data["summary"]["pending_tasks"] >= 1
    assert 0 <= data["completion_rate"] <= 100


def test_dashboard_requires_authentication(client):
    response = client.get("/analytics/dashboard?days=7")

    assert response.status_code == 401


def test_dashboard_rejects_invalid_days(client, auth_headers):
    response = client.get(
        "/analytics/dashboard?days=0",
        headers=auth_headers,
    )

    assert response.status_code == 422