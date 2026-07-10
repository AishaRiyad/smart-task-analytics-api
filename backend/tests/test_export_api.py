def create_test_task(client, auth_headers):
    response = client.post(
        "/tasks/",
        json={
            "title": "Export test task",
            "description": "Task used for export tests",
            "completed": True,
            "completion_time": 25,
        },
        headers=auth_headers,
    )

    assert response.status_code == 201


def test_export_tasks_csv(client, auth_headers):
    create_test_task(client, auth_headers)

    response = client.get(
        "/tasks/export/csv",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "attachment" in response.headers["content-disposition"]
    assert "tasks.csv" in response.headers["content-disposition"]
    assert b"Export test task" in response.content


def test_export_tasks_excel(client, auth_headers):
    create_test_task(client, auth_headers)

    response = client.get(
        "/tasks/export/excel",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert (
        response.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    assert "attachment" in response.headers["content-disposition"]
    assert "tasks.xlsx" in response.headers["content-disposition"]

    assert response.content[:2] == b"PK"


def test_export_tasks_pdf(client, auth_headers):
    create_test_task(client, auth_headers)

    response = client.get(
        "/tasks/export/pdf",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    assert "tasks.pdf" in response.headers["content-disposition"]

    assert response.content.startswith(b"%PDF")


def test_export_requires_authentication(client):
    csv_response = client.get("/tasks/export/csv")
    excel_response = client.get("/tasks/export/excel")
    pdf_response = client.get("/tasks/export/pdf")

    assert csv_response.status_code == 401
    assert excel_response.status_code == 401
    assert pdf_response.status_code == 401