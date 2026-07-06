import statistics
import time
import requests

BASE_URL = "http://localhost:8000"

payload = {
    "title": "Benchmark",
    "description": "Performance Test",
    "completed": False,
    "completion_time": None
}


def benchmark(endpoint):
    times = []

    for _ in range(20):
        start = time.perf_counter()

        requests.post(BASE_URL + endpoint, json=payload)

        end = time.perf_counter()

        times.append(end - start)

    print(endpoint)
    print("Average:", round(statistics.mean(times), 4))
    print()


benchmark("/tasks/sync-email")
benchmark("/tasks/")