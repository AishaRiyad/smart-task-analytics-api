from locust import HttpUser, task, between

AUTH_HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc4MzYzMzYyOX0.1NeMDRsMYuguxZiVFYNqGLdbggricivHE_2WnsaPBAw"
}


class AnalyticsWithoutCacheUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def analytics_without_cache(self):
        self.client.get(
            "/analytics/summary",
            headers=AUTH_HEADERS
        )


class AnalyticsWithCacheUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def analytics_with_cache(self):
        self.client.get(
            "/analytics/summary-cached",
            headers=AUTH_HEADERS
        )


class SyncEmailUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def create_task_sync_email(self):
        self.client.post("/tasks/sync-email", json={
            "title": "Sync email benchmark task",
            "description": "Created by Locust baseline test",
            "completed": False,
            "completion_time": None
        }, headers=AUTH_HEADERS)


class BackgroundEmailUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def create_task_background_email(self):
        self.client.post("/tasks/", json={
            "title": "Background email benchmark task",
            "description": "Created by Locust optimized test",
            "completed": False,
            "completion_time": None
        }, headers=AUTH_HEADERS)


class SyncExternalUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def sync_external_api(self):
        self.client.get(
            "/external/weather-sync",
            headers=AUTH_HEADERS
        )


class AsyncExternalUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def async_external_api(self):
        self.client.get(
            "/external/weather-async",
            headers=AUTH_HEADERS
        )