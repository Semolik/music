import json
from fastapi.testclient import TestClient

# cookies = {}


def test_create_user(client: TestClient):

    data = {
        "username": "testuser2",
        "password": "testpassword2",
        "first_name": "test_name2",
        "last_name": "test_last_name2"
    }
    response = client.post("/auth/signup", json.dumps(data))

    global cookies
    cookies = response.cookies

    assert response.status_code == 201
