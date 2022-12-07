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
