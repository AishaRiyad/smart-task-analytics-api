import statistics
import time
import requests

BASE_URL = "http://localhost:8000"
REQUESTS = 30


def benchmark(endpoint: str):
    times = []

    for _ in range(REQUESTS):
        start = time.perf_counter()
        response = requests.get(BASE_URL + endpoint)
        end = time.perf_counter()

        assert response.status_code == 200
        times.append(end - start)

    return {
        "endpoint": endpoint,
        "requests": REQUESTS,
        "average": round(statistics.mean(times), 4),
        "min": round(min(times), 4),
        "max": round(max(times), 4),
    }


if __name__ == "__main__":
    without_cache = benchmark("/analytics/summary")
    with_cache = benchmark("/analytics/summary-cached")

    print("Without Cache:", without_cache)
    print("With Cache:", with_cache)