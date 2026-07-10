from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

BASE_URL = "http://localhost:8000"

USER_DATA = {
    "username": "loadtestuser",
    "email": "loadtestuser@example.com",
    "password": "testpassword123"
}


def register_user() -> None:
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=USER_DATA,
        timeout=10
    )


    if response.status_code not in (200, 201, 400, 409):
        raise RuntimeError(
            f"Registration failed: "
            f"{response.status_code} - {response.text}"
        )


def get_token() -> str:
    register_user()

    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": USER_DATA["username"],
            "password": USER_DATA["password"]
        },
        timeout=10
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Login failed: "
            f"{response.status_code} - {response.text}"
        )

    return response.json()["access_token"]


def send_request(headers: dict[str, str]) -> int:
    try:
        response = requests.get(
            f"{BASE_URL}/tasks/",
            headers=headers,
            timeout=10
        )
        return response.status_code

    except requests.RequestException:
        return 0


def main():
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    total_requests = 1000
    concurrent_workers = 30

    with ThreadPoolExecutor(
        max_workers=concurrent_workers
    ) as executor:
        futures = [
            executor.submit(send_request, headers)
            for _ in range(total_requests)
        ]

        results = [
            future.result()
            for future in as_completed(futures)
        ]

    successful = sum(status == 200 for status in results)
    unauthorized = sum(status == 401 for status in results)
    failed = len(results) - successful

    print(f"Completed: {len(results)} requests")
    print(f"Successful: {successful}")
    print(f"Unauthorized: {unauthorized}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()