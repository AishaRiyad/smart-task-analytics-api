# Performance Benchmark Results

## Environment

- Users: 20
- Spawn Rate: 5 users/second
- Tool: Locust
- Backend: FastAPI
- Database: PostgreSQL
- Cache: Redis
- Containerization: Docker Compose

---

# Experiment 1: Redis Cache

## Goal

Measure the effect of Redis caching on analytics response time.

## Results

| Version | Endpoint | Requests | Avg Response Time | Min | Max | Median | Requests/sec | Failures |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Without Cache | `/analytics/summary` | 393 | 512 ms | 505 ms | 677 ms | 510 ms | 9.66 | 0 |
| With Redis Cache | `/analytics/summary-cached` | 541 | 10 ms | 1 ms | 617 ms | 4 ms | 12.88 | 0 |

## Conclusion

Redis caching significantly improved analytics performance. The average response time decreased from 512 ms to 10 ms because repeated requests were served from Redis instead of recalculating analytics from the database.

---

# Experiment 2: Background Tasks

## Goal

Compare sending a fake email before the response versus using FastAPI BackgroundTasks.

## Results

| Version | Endpoint | Requests | Avg Response Time | Min | Max | Median | Requests/sec | Failures |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Sync Email | `/tasks/sync-email` | 400 | 3050 ms | 3007 ms | 3502 ms | 3100 ms | 4.30 | 0 |
| BackgroundTasks | `/tasks/` | 305 | 2384 ms | 22 ms | 12274 ms | 1800 ms | 4.99 | 0 |

## Conclusion

BackgroundTasks reduced the average response time compared with synchronous email sending, but the improvement was not as large as expected under 20 concurrent users. This happened because the fake email function still uses blocking `time.sleep(3)`, and many concurrent background tasks can saturate available worker threads. However, the minimum response time shows that the response can return quickly when background processing is not congested.

---

# Experiment 3: Sync vs Async External API

## Goal

Compare synchronous and asynchronous external API simulation under concurrent load.

## Results

| Version | Endpoint | Requests | Avg Response Time | Min | Max | Median | Requests/sec | Failures |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Sync External API | `/external/weather-sync` | 197 | 2006 ms | 2002 ms | 2054 ms | 2002 ms | 5.51 | 0 |
| Async External API | `/external/weather-async` | 250 | 2005 ms | 2001 ms | 2022 ms | 2001 ms | 5.52 | 0 |

## Conclusion

The sync and async endpoints showed similar average response time because both endpoints simulate a fixed 2-second delay. The async version handled slightly more requests during the same load test, but the difference was small. A more realistic external HTTP call or higher concurrency would show the benefit of async programming more clearly.

---

# Experiment 4: Middleware Timing

## Goal

Measure request processing time for each response.

## Implementation

Every API response includes:

```text
X-Process-Time