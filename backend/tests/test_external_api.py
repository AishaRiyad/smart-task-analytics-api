import pytest


@pytest.mark.asyncio
async def test_weather_sync(client):
    response = await client.get("/external/weather-sync")

    assert response.status_code == 200
    assert response.json()["type"] == "sync"


@pytest.mark.asyncio
async def test_weather_async(client):
    response = await client.get("/external/weather-async")

    assert response.status_code == 200
    assert response.json()["type"] == "async"