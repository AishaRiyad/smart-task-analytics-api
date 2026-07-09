# Smart Task & Analytics API

![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

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


## Authentication

The application uses JWT (JSON Web Tokens) to secure protected endpoints.

### Authentication Flow

```text
Register
    │
    ▼
Login
    │
    ▼
Access Token (15 min)
    │
    ▼
Refresh Token (7 days)
    │
    ▼
Protected Endpoints
```

### Authentication Features

- User registration
- Secure login
- JWT Access Token authentication
- Refresh Token support
- Protected API endpoints
- User identity verification
- Task ownership authorization

---

## Features

### Core Features

- Task CRUD API
- Task Search
- Analytics Summary

### Authentication

- JWT Authentication
- Access Token
- Refresh Token
- Authorization
- Protected Endpoints
- Task Ownership Validation

### Performance Features

- Redis Caching
- Background Tasks
- Async Programming
- Request Timing Middleware
- GZip Compression
- Pagination
- Connection Pool Tuning
- PostgreSQL Full-text Search

### Testing Strategy

- API Testing
- Integration Testing
- PostgreSQL Container Testing
- Redis Container Testing
- Mocking Tests
- Performance Testing using Locust
- Swagger API Documentation
---



## Performance Optimizations

### Pagination

Pagination limits the number of returned records per request, reducing database load and improving response time for large datasets.

### Connection Pool

SQLAlchemy connection pooling reuses existing database connections instead of creating a new connection for every request, improving scalability under concurrent traffic.

### GZip Compression

GZip middleware compresses HTTP responses before sending them to clients, reducing bandwidth usage and improving response transfer speed.

### Search Optimization

The application supports Prefix Search, Contains Search, and PostgreSQL Full-text Search to provide fast and efficient text searching depending on the query type.

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
│   │   │       ├── auth.py
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
│   │   │   ├── task.py
│   │   │   └── user.py
│   │   │
│   │   ├── services/
│   │   │   ├── analytics_service.py
│   │   │   ├── auth_service.py
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

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| POST | `/tasks/` | Create a new task using BackgroundTasks |
| POST | `/tasks/sync-email` | Create a task and send fake email before response |
| GET | `/tasks/` | Get all tasks |
| GET | `/tasks/?page=1&size=20` | Get paginated task listing |
| GET | `/tasks/{id}` | Get task by ID |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/tasks/search/?keyword=value` | Search tasks by title or description |
| GET | `/tasks/full-text-search/?keyword=value` | PostgreSQL full-text search |

---

# Authentication

The API is secured using JWT authentication. Users must authenticate before accessing protected resources.

| Method | Endpoint | Description |
|------|------|------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive access & refresh tokens |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/users/me` | Get current authenticated user |

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

### Authorization

Each user can only manage their own tasks and comments.

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

The application uses PostgreSQL as the main relational database.

The database currently contains two main tables:

```text
users
tasks
```

### Database Entities

#### users

Stores registered users and authentication-related data.

**User fields:**

- id
- username
- email
- hashed_password

#### tasks

Stores task information created by users.

**Task fields:**

- id
- title
- description
- completed
- completion_time
- owner_id
- created_at
- updated_at

---

### Database Relationships

```text
User
 │
 └──────────────< Task
```

### Relationship Summary

- One **User** can create many **Tasks**.
- Each **Task** belongs to exactly one **User**.

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

### Benchmark After Optimization

| Version | Requests | Avg | Min | Max | Median | RPS | Failures |
|------|------:|------:|------:|------:|------:|------:|------:|
| Without Cache | 588 | 510.34 ms | 504 ms | 719 ms | 510 ms | 10.4 | 0 |
| With Redis Cache | 789 | 9.05 ms | 2 ms | 612 ms | 5 ms | 13.1 | 0 |

The optimized implementation further improved throughput while maintaining the same functionality.


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

### Benchmark After Authentication Improvements

| Version | Requests | Avg | Min | Max | Median | RPS | Failures |
|------|------:|------:|------:|------:|------:|------:|------:|
| Sync Email | 252 | 3047.9 ms | 3013 ms | 3155 ms | 3100 ms | 4.8 | 0 |
| BackgroundTasks | 584 | 499.19 ms | 12 ms | 1549 ms | 460 ms | 9.2 | 0 |


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

### Benchmark After Optimization

| Version | Requests | Avg | Min | Max | Median | RPS | Failures |
|------|------:|------:|------:|------:|------:|------:|------:|
| Sync | 335 | 2006.83 ms | 2003 ms | 2059 ms | 2002.72 ms | 6 | 0 |
| Async | 329 | 2006.26 ms | 2002 ms | 2074 ms | 2001.57 ms | 5.3 | 0 |


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

## Benchmark Comparison

| Feature | Before | After | Improvement |
|----------|--------:|-------:|-------------|
| Redis Cache | 512 ms | 9 ms | ~98% faster |
| Background Email | 2384 ms | 499 ms | ~79% faster |
| Pagination | N/A | 10.55 ms | Added |
| Prefix Search | N/A | 6.17 ms | Added |
| Contains Search | N/A | 4.19 ms | Added |
| Full-text Search | N/A | 8.28 ms | Added |
| JWT Authentication | Open | Protected | Security Improved |

---

## Performance Improvements

| Improvement | Purpose |
|-------------|---------|
| Redis Cache | Reduce analytics response time |
| Background Tasks | Move email processing outside the request-response cycle |
| Async Programming | Improve I/O concurrency |
| Pagination | Reduce database load |
| Connection Pool | Reuse database connections efficiently |
| GZip Compression | Reduce HTTP response size |
| PostgreSQL Full-text Search | Faster and more efficient text searching |
| JWT Authentication | Secure protected endpoints |

---

## Testing Strategy

| Test Type | Framework |
|-----------|-----------|
| Unit Tests | Pytest |
| API Tests | FastAPI TestClient |
| Integration Tests | Testcontainers |
| PostgreSQL Tests | Testcontainers |
| Redis Tests | Testcontainers |
| Mock Tests | unittest.mock |
| Load Tests | Locust |
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

## Pagination Benchmark

| Metric | Value |
|------|------:|
| Average | 10.55 ms |
| Minimum | 3.94 ms |
| Maximum | 147.82 ms |

---

## Search Benchmark

| Search Type | Average |
|------|------:|
| Prefix Search | 6.17 ms |
| Contains Search | 4.19 ms |
| Full-text Search | 8.28 ms |

---

## Authentication Protection

Unauthenticated requests correctly returned **401 Unauthorized**.

| Endpoint | Result |
|------|------|
| GET /tasks/ | 401 |
| POST /tasks/ | 401 |
| GET /tasks/search/?keyword=Performance | 401 |


---

# Discussion Summary

Smart Task & Analytics API is a FastAPI backend application built to demonstrate secure API development, testing, and performance optimization. The application supports task CRUD operations, search, analytics, Redis caching, background tasks, middleware timing, sync/async external API simulation, JWT authentication, pagination, GZip compression, and database connection pool tuning.

The benchmark results demonstrate that caching produced the largest performance gain, reducing analytics response time from more than 500 ms to approximately 9 ms. Background tasks also improved response time by moving email processing outside the request-response cycle.

Pagination, connection pooling, response compression, and PostgreSQL Full-text Search improved scalability and resource utilization. Authentication introduced secure access control using access and refresh tokens without significantly affecting application performance.

The project also includes API, integration, PostgreSQL container, Redis container, mocking, and Locust performance tests to verify correctness, reliability, and performance under load.

---

## Future Improvements

- Role-Based Authorization (Admin/User)
- Advanced Filtering and Sorting
- Prometheus Metrics
- Grafana Dashboard
- CI/CD using GitHub Actions
- Kubernetes Deployment
- Rate Limiting
- Real External Weather API Integration
- Message Queue (RabbitMQ/Celery) for Email Processing

---

# Author

* Aesha Abu Jeeb

---

# License

This project was developed for educational purposes to demonstrate backend API development, testing, and performance optimization using FastAPI.