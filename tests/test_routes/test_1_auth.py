import json
from fastapi.testclient import TestClient

data = {
    "username": "testuser2",
    "password": "testpassword2",
    "first_name": "test_name2",
    "last_name": "test_last_name2"
}


def test_create_user_and_user_with_same_username(client: TestClient):
    response = client.post("/auth/signup", json.dumps(data))
    assert response.status_code == 201
    global cookies
    cookies = response.cookies

    response = client.post("/auth/signup", json.dumps(data))
    assert response.status_code == 400


def test_logout(client: TestClient):
    response = client.delete("/auth/logout", cookies=cookies)

    assert response.status_code == 200


def test_get_refresh_token(client: TestClient):
    response = client.post("/auth/refresh", cookies=cookies)

    assert response.status_code == 200
