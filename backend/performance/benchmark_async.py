import statistics
import time
import requests

BASE_URL = "http://localhost:8000"


def benchmark(endpoint):
    times = []

    for _ in range(20):
        start = time.perf_counter()

        requests.get(BASE_URL + endpoint)

        end = time.perf_counter()

        times.append(end - start)

    print(endpoint)
    print("Average:", round(statistics.mean(times), 4))


benchmark("/external/weather-sync")
benchmark("/external/weather-async")