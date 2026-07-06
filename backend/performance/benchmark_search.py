import statistics
import time

import requests

BASE_URL = "http://localhost:8000"
REQUESTS = 30


times = []

for _ in range(REQUESTS):

    start = time.perf_counter()

    requests.get(
        BASE_URL + "/tasks/search/?keyword=Performance"
    )

    end = time.perf_counter()

    times.append(end - start)

print("Average:", statistics.mean(times))