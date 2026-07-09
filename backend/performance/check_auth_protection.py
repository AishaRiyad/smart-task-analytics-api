import requests

BASE_URL = "http://localhost:8000"

endpoints = [
    ("GET", "/tasks/"),
    ("POST", "/tasks/"),
    ("GET", "/tasks/search/?keyword=Performance"),
]

for method, endpoint in endpoints:
    if method == "GET":
        response = requests.get(BASE_URL + endpoint)
    else:
        response = requests.post(BASE_URL + endpoint, json={
            "title": "Unauthorized task",
            "description": "Should fail",
            "completed": False,
            "completion_time": None
        })

    print(method, endpoint, response.status_code)