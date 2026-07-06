import time
import requests


BASE_URL = "http://localhost:8000"
REQUESTS_COUNT = 50


def benchmark_endpoint(endpoint: str):
    times = []

    for _ in range(REQUESTS_COUNT):
        start = time.perf_counter()
        response = requests.get(f"{BASE_URL}{endpoint}")
        end = time.perf_counter()

        assert response.status_code == 200
        times.append(end - start)

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    return {
        "endpoint": endpoint,
        "requests": REQUESTS_COUNT,
        "average_time_seconds": round(avg_time, 4),
        "min_time_seconds": round(min_time, 4),
        "max_time_seconds": round(max_time, 4),
    }


if __name__ == "__main__":
    print("Benchmark: Analytics without cache")
    no_cache_result = benchmark_endpoint("/analytics/summary")
    print(no_cache_result)

    print("\nBenchmark: Analytics with Redis cache")
    cached_result = benchmark_endpoint("/analytics/summary-cached")
    print(cached_result)