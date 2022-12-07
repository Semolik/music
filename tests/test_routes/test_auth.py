import json
from fastapi.testclient import TestClient

# cookies = {}


def test_create_user(client: TestClient):

    data = {
        "username": "testuser",
        "password": "testpassword",
        "first_name": "test_name",
        "last_name": "test_last_name"
    }
    response = client.post("/signup", json.dumps(data))

    global cookies
    cookies = response.cookies

    assert response.status_code == 201


def test_update_user_info(client: TestClient, normal_user_token_cookies):

    data = {
        "first_name": "",
        "last_name": "test_last_name",
        "remove_picture": False
    }
    print(normal_user_token_cookies)
    response = client.put(
        "/me", data=data, cookies=normal_user_token_cookies)
    assert response.status_code == 200
