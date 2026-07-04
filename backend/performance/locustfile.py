from locust import HttpUser, task, between


class SmartTaskUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_tasks(self):
        self.client.get("/tasks/")

    @task(2)
    def search_tasks(self):
        self.client.get("/tasks/search/?keyword=Performance")

    @task(2)
    def analytics_summary(self):
        self.client.get("/analytics/summary")

    @task(2)
    def cached_analytics_summary(self):
        self.client.get("/analytics/summary-cached")

    @task(1)
    def create_task(self):
        self.client.post("/tasks/", json={
            "title": "Locust performance task",
            "description": "Created during load testing",
            "completed": False,
            "completion_time": None
        })

    @task(1)
    def external_async(self):
        self.client.get("/external/weather-async")