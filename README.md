# Smart Task & Analytics API

## Overview

Smart Task & Analytics API is a FastAPI-based backend project designed to demonstrate API development and performance optimization concepts through practical experiments.

The application allows users to manage tasks, search tasks, generate analytics, simulate external API calls, and compare performance before and after applying optimization techniques.

The main goal of this project is not only to build CRUD endpoints, but also to measure performance using benchmarks and improve the application based on real results.

---

## Main Idea

The project follows a performance experiment approach:

```text
Baseline
   ↓
Measure Performance
   ↓
Apply Optimization
   ↓
Measure Again
   ↓
Compare Results
```

This approach was used to test:

* Redis caching
* Background tasks
* Async vs sync execution
* Middleware timing
* Load testing

---

## Features

* Task CRUD API
* Task Search
* Analytics Summary
* Redis Caching
* Cache Invalidation
* Sync vs Async External API Simulation
* Background Email Notification
* Request Timing Middleware
* PostgreSQL Database
* Docker Compose Setup
* API Testing
* Integration Testing
* PostgreSQL Container Testing
* Redis Container Testing
* Mocking Tests
* Load Testing with Locust
* Swagger API Documentation

---

## Technologies Used

* Python 3.11
* FastAPI
* PostgreSQL
* SQLAlchemy
* Redis
* Docker
* Docker Compose
* Pytest
* Testcontainers
* Locust
* Pydantic

---

## Project Structure

```text
smart-task-analytics-api/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── analytics.py
│   │   │       ├── external.py
│   │   │       └── tasks.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── middleware.py
│   │   │
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── models.py
│   │   │
│   │   ├── schemas/
│   │   │   └── task.py
│   │   │
│   │   ├── services/
│   │   │   ├── analytics_service.py
│   │   │   ├── cache_service.py
│   │   │   ├── email_service.py
│   │   │   └── external_service.py
│   │   │
│   │   ├── utils/
│   │   │   └── seed_tasks.py
│   │   │
│   │   └── main.py
│   │
│   ├── performance/
│   │   ├── locustfile.py
│   │   ├── benchmark_results.md
│   │   └── screenshots/
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_tasks_api.py
│   │   ├── test_analytics_api.py
│   │   ├── test_external_api.py
│   │   ├── test_database_container.py
│   │   ├── test_integration_api_database.py
│   │   ├── test_redis_container.py
│   │   └── test_mocking_services.py
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Application Architecture

```text
Client
  ↓
FastAPI Routes
  ↓
Services
  ↓
SQLAlchemy ORM
  ↓
PostgreSQL
```

For cached analytics:

```text
Client
  ↓
FastAPI
  ↓
Redis Cache
  ↓
PostgreSQL only if cache is missing
```

---

## API Endpoints

### Tasks

| Method | Endpoint                       | Description                                       |
| ------ | ------------------------------ | ------------------------------------------------- |
| POST   | `/tasks/`                      | Create a new task using BackgroundTasks           |
| POST   | `/tasks/sync-email`            | Create a task and send fake email before response |
| GET    | `/tasks/`                      | Get all tasks                                     |
| GET    | `/tasks/{id}`                  | Get task by ID                                    |
| PUT    | `/tasks/{id}`                  | Update task                                       |
| DELETE | `/tasks/{id}`                  | Delete task                                       |
| GET    | `/tasks/search/?keyword=value` | Search tasks by title or description              |

---

### Analytics

| Method | Endpoint                    | Description                                |
| ------ | --------------------------- | ------------------------------------------ |
| GET    | `/analytics/summary`        | Calculate analytics directly from database |
| GET    | `/analytics/summary-cached` | Return analytics using Redis cache         |

---

### External API Simulation

| Method | Endpoint                  | Description                             |
| ------ | ------------------------- | --------------------------------------- |
| GET    | `/external/weather-sync`  | Simulate synchronous external API call  |
| GET    | `/external/weather-async` | Simulate asynchronous external API call |

---

## Database

The application uses PostgreSQL as the main database.

Main table:

```text
tasks
```

Task fields:

* id
* title
* description
* completed
* completion_time
* created_at
* updated_at

---

## Redis Caching

Redis is used to cache analytics results.

Flow:

```text
First request:
Database → Calculate analytics → Store in Redis → Return response

Next requests:
Redis → Return cached response
```

Cache is invalidated when a task is:

* Created
* Updated
* Deleted

This prevents stale analytics data.

---

## Background Tasks

The application simulates sending an email after creating a task.

Two versions are provided:

| Version   | Endpoint            | Behavior                                                    |
| --------- | ------------------- | ----------------------------------------------------------- |
| Baseline  | `/tasks/sync-email` | Sends fake email before returning response                  |
| Optimized | `/tasks/`           | Returns response first, then sends fake email in background |

This demonstrates how non-critical work can be moved outside the request-response cycle.

---

## Async vs Sync Simulation

The project includes two external API simulation endpoints:

| Version | Endpoint                  |
| ------- | ------------------------- |
| Sync    | `/external/weather-sync`  |
| Async   | `/external/weather-async` |

The goal is to demonstrate the difference between blocking and non-blocking operations, especially under concurrent load.

---

## Middleware Timing

Every API response includes:

```text
X-Process-Time
```

This header shows how long the request took to process.

Example:

```text
X-Process-Time: 0.034
```

---

# Performance Benchmark Results

Load testing was performed using Locust.

Test configuration:

* Users: 20
* Spawn rate: 5 users/second
* Tool: Locust
* Backend: FastAPI
* Database: PostgreSQL
* Cache: Redis
* Environment: Docker Compose

---

## Experiment 1: Redis Cache

### Goal

Measure the effect of Redis caching on analytics response time.

### Results

| Version          | Endpoint                    | Requests | Avg Response Time |    Min |    Max | Median | Requests/sec | Failures |
| ---------------- | --------------------------- | -------: | ----------------: | -----: | -----: | -----: | -----------: | -------: |
| Without Cache    | `/analytics/summary`        |      393 |            512 ms | 505 ms | 677 ms | 510 ms |         9.66 |        0 |
| With Redis Cache | `/analytics/summary-cached` |      541 |             10 ms |   1 ms | 617 ms |   4 ms |        12.88 |        0 |

### Conclusion

Redis caching significantly improved analytics performance. The average response time decreased from 512 ms to 10 ms because repeated requests were served from Redis instead of recalculating analytics from the database.

---

## Experiment 2: Background Tasks

### Goal

Compare sending a fake email before the response versus using FastAPI BackgroundTasks.

### Results

| Version         | Endpoint            | Requests | Avg Response Time |     Min |      Max |  Median | Requests/sec | Failures |
| --------------- | ------------------- | -------: | ----------------: | ------: | -------: | ------: | -----------: | -------: |
| Sync Email      | `/tasks/sync-email` |      400 |           3050 ms | 3007 ms |  3502 ms | 3100 ms |         4.30 |        0 |
| BackgroundTasks | `/tasks/`           |      305 |           2384 ms |   22 ms | 12274 ms | 1800 ms |         4.99 |        0 |

### Conclusion

BackgroundTasks reduced the average response time compared with synchronous email sending, but the improvement was not as large as expected under 20 concurrent users. This happened because the fake email function uses a blocking delay, and many concurrent background jobs can saturate available worker threads.

---

## Experiment 3: Sync vs Async External API

### Goal

Compare synchronous and asynchronous external API simulation under concurrent load.

### Results

| Version            | Endpoint                  | Requests | Avg Response Time |     Min |     Max |  Median | Requests/sec | Failures |
| ------------------ | ------------------------- | -------: | ----------------: | ------: | ------: | ------: | -----------: | -------: |
| Sync External API  | `/external/weather-sync`  |      197 |           2006 ms | 2002 ms | 2054 ms | 2002 ms |         5.51 |        0 |
| Async External API | `/external/weather-async` |      250 |           2005 ms | 2001 ms | 2022 ms | 2001 ms |         5.52 |        0 |

### Conclusion

The sync and async endpoints showed similar average response time because both simulate a fixed 2-second delay. The async version handled slightly more requests during the same load test, but the difference was small. A more realistic external HTTP call or higher concurrency would show the benefit of async programming more clearly.

---

## Experiment 4: Middleware Timing

### Goal

Measure request processing time for every API response.

### Result

Every response includes:

```text
X-Process-Time
```

### Conclusion

The middleware helps monitor API response time directly from response headers.

---

# Testing Strategy

The project includes several types of tests.

## API Tests

API tests verify that endpoints return correct responses.

Examples:

* Create task
* Get tasks
* Search tasks
* Get analytics
* Test external endpoints
* Test not found cases

---

## Integration Tests

Integration tests verify the full flow:

```text
TestClient
  ↓
FastAPI
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

These tests check that API endpoints work correctly with the database.

---

## PostgreSQL Container Tests

Database tests use a real PostgreSQL container through Testcontainers.

This means the database tests are not mocked.

They verify:

* Create task
* Read task
* PostgreSQL connection
* SQLAlchemy model behavior

---

## Redis Container Tests

Redis tests use a real Redis container.

They verify:

* Set cache value
* Get cache value
* Delete cache value

---

## Mocking Tests

Mocks are used for external or non-critical services such as:

* Email service
* External API service

This avoids depending on real external systems during unit tests.

---

# Running the Project

## 1. Start Docker Services

```bash
docker compose up --build
```

---

## 2. Open Swagger Documentation

```text
http://localhost:8000/docs
```

---

## 3. Seed the Database

```bash
docker compose exec backend python -m app.utils.seed_tasks
```

---

## 4. Run Tests

```bash
docker compose exec backend pytest
```

---

## 5. Run Locust Load Testing

```bash
docker compose exec backend locust -f performance/locustfile.py AnalyticsWithoutCacheUser --host http://localhost:8000
```

Open Locust UI:

```text
http://localhost:8089
```

---

# Locust Experiment Commands

## Analytics Without Cache

```bash
docker compose exec backend locust -f performance/locustfile.py AnalyticsWithoutCacheUser --host http://localhost:8000
```

## Analytics With Redis Cache

```bash
docker compose exec backend locust -f performance/locustfile.py AnalyticsWithCacheUser --host http://localhost:8000
```

## Sync Email

```bash
docker compose exec backend locust -f performance/locustfile.py SyncEmailUser --host http://localhost:8000
```

## Background Email

```bash
docker compose exec backend locust -f performance/locustfile.py BackgroundEmailUser --host http://localhost:8000
```

## Sync External API

```bash
docker compose exec backend locust -f performance/locustfile.py SyncExternalUser --host http://localhost:8000
```

## Async External API

```bash
docker compose exec backend locust -f performance/locustfile.py AsyncExternalUser --host http://localhost:8000
```

---

# Discussion Summary

Smart Task & Analytics API is a FastAPI backend application built to demonstrate performance optimization concepts. The application supports task CRUD operations, search, analytics, Redis caching, background tasks, middleware timing, and sync/async external API simulation.

Performance was measured using Locust. The strongest improvement appeared in the Redis caching experiment, where average analytics response time decreased from 512 ms to 10 ms. Background tasks also showed improvement, but the results were affected by blocking fake email simulation under concurrent load. The async experiment showed similar response time to sync because both endpoints simulate a fixed delay, but the async version handled slightly more requests.

The project also includes API, integration, database container, Redis container, and mocking tests to verify correctness and reliability.

---

# Future Improvements

* Add JWT authentication
* Add role-based authorization
* Add pagination for task listing
* Add advanced filtering
* Add database indexing benchmark
* Add Prometheus metrics
* Add Grafana dashboard
* Add GitHub Actions CI pipeline
* Add frontend dashboard
* Add real external API integration
* Improve async benchmark with real concurrent HTTP calls

---

# Author

* Aesha Abu Jeeb

---

# License

This project was developed for educational purposes to demonstrate backend API development, testing, and performance optimization using FastAPI.
