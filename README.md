# Smart Task & Analytics API

## Overview

Smart Task & Analytics API is a FastAPI-based backend application developed to demonstrate modern API development and performance optimization techniques.

The application allows users to manage tasks through CRUD operations, search tasks, generate analytics, simulate external API calls, and evaluate different performance optimization strategies such as caching, asynchronous programming, middleware timing, and background tasks.

This project is designed for learning and demonstrating software performance concepts rather than only implementing CRUD operations.

---

# Features

* Task CRUD API
* Task Search
* Analytics Summary
* Redis Caching
* Async vs Sync External API Simulation
* Background Email Notification
* Request Timing Middleware
* PostgreSQL Database
* Docker Compose Environment
* Load Testing with Locust
* RESTful API Documentation using Swagger

---

# Technologies Used

* FastAPI
* Python 3.11
* PostgreSQL
* SQLAlchemy
* Redis
* Docker
* Docker Compose
* Pytest
* Locust
* Pydantic

---

# Project Structure

```text
smart-task-analytics/
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
│   │   └── results.md
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_tasks_api.py
│   │   ├── test_analytics_api.py
│   │   └── test_external_api.py
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

# API Endpoints

## Tasks

| Method | Endpoint                       | Description       |
| ------ | ------------------------------ | ----------------- |
| POST   | `/tasks/`                      | Create a new task |
| GET    | `/tasks/`                      | Get all tasks     |
| GET    | `/tasks/{id}`                  | Get task by ID    |
| PUT    | `/tasks/{id}`                  | Update task       |
| DELETE | `/tasks/{id}`                  | Delete task       |
| GET    | `/tasks/search/?keyword=value` | Search tasks      |

---

## Analytics

| Method | Endpoint                    | Description                          |
| ------ | --------------------------- | ------------------------------------ |
| GET    | `/analytics/summary`        | Generate analytics from database     |
| GET    | `/analytics/summary-cached` | Generate analytics using Redis cache |

---

## External API Simulation

| Method | Endpoint                  | Description                        |
| ------ | ------------------------- | ---------------------------------- |
| GET    | `/external/weather-sync`  | Simulate synchronous external API  |
| GET    | `/external/weather-async` | Simulate asynchronous external API |

---

# Performance Features

## Middleware Timing

Every response contains:

```text
X-Process-Time
```

This header measures the total processing time of each request.

---

## Redis Caching

Analytics responses are cached for 60 seconds.

Flow:

```text
Request
      │
      ▼
Redis Cache?
   │
   ├── Yes → Return Cached Result
   │
   └── No
         │
         ▼
   PostgreSQL
         │
         ▼
Calculate Summary
         │
         ▼
Store in Redis
         │
         ▼
Return Response
```

---

## Background Tasks

Whenever a new task is created:

* Response is returned immediately.
* Fake email notification is executed in the background.

---

## Async Programming

The project demonstrates the difference between:

* Synchronous API calls
* Asynchronous API calls

using simulated external services.

---

# Database

Database:

* PostgreSQL

ORM:

* SQLAlchemy

Main table:

```text
tasks
```

Columns:

* id
* title
* description
* completed
* completion_time
* created_at
* updated_at

---

# Load Testing

Load testing is implemented using Locust.

Tested endpoints include:

* GET /tasks
* POST /tasks
* GET /tasks/search
* GET /analytics/summary
* GET /analytics/summary-cached
* GET /external/weather-async

Measured metrics:

* Response Time
* Requests Per Second
* Error Rate

---

# Testing

The project contains API tests for:

* Task CRUD
* Analytics
* External API
* Error handling

Tests are executed using:

```bash
pytest
```

---

# Running the Project

## Start Docker

```bash
docker compose up --build
```

---

## Open Swagger

```text
http://localhost:8000/docs
```

---

## Seed Database

```bash
docker compose exec backend python -m app.utils.seed_tasks
```

---

## Run Tests

```bash
docker compose exec backend pytest
```

---

## Run Load Test

```bash
docker compose exec backend locust -f performance/locustfile.py --host http://localhost:8000
```

Open:

```text
http://localhost:8089
```

---

# Future Improvements

* User Authentication (JWT)
* Role-Based Authorization
* Pagination
* Advanced Filtering
* Rate Limiting
* Prometheus Metrics
* Grafana Dashboard
* CI/CD Pipeline using GitHub Actions

---

# Authors

* Aesha Abu Jeeb

---

# License

This project was developed for educational purposes to demonstrate backend API development and performance optimization techniques using FastAPI.
