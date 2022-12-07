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

    assert "access_token_cookie" in response.headers['set-cookie']

    assert response.status_code == 201


def test_update_user_info(client: TestClient):

    data = {
        "first_name": "",
        "last_name": "test_last_name",
        "remove_picture": False
    }
    response = client.put(
        "/me", data=data, cookies={'access_token_cookie': cookies['access_token_cookie']})
    assert response.status_code == 200
