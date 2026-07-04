def test_weather_sync(client):
    response = client.get("/external/weather-sync")

    assert response.status_code == 200
    assert response.json()["type"] == "sync"


def test_weather_async(client):
    response = client.get("/external/weather-async")

    assert response.status_code == 200
    assert response.json()["type"] == "async"