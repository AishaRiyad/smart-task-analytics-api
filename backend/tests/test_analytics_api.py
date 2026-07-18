async def test_analytics_summary(client, auth_headers):
    response = await client.get(
        "/analytics/summary",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert "total_tasks" in response.json()
    assert "completed_tasks" in response.json()
    assert "pending_tasks" in response.json()
    assert "average_completion_time" in response.json()


async def test_cached_analytics_summary(client, auth_headers):
    response = await client.get(
        "/analytics/summary-cached",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert "source" in response.json()