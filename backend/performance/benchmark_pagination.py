import statistics
import time
import requests

BASE_URL = "http://localhost:8000"
REQUESTS = 30

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc4MzYzMzYyOX0.1NeMDRsMYuguxZiVFYNqGLdbggricivHE_2WnsaPBAw"


def benchmark(endpoint):
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    times = []

    for _ in range(REQUESTS):
        start = time.perf_counter()
        response = requests.get(BASE_URL + endpoint, headers=headers)
        end = time.perf_counter()

        assert response.status_code == 200
        times.append(end - start)

    print(endpoint)
    print("Requests:", REQUESTS)
    print("Average:", round(statistics.mean(times) * 1000, 2), "ms")
    print("Min:", round(min(times) * 1000, 2), "ms")
    print("Max:", round(max(times) * 1000, 2), "ms")


if __name__ == "__main__":
    benchmark("/tasks/?page=1&size=20")