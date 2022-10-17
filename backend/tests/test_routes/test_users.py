import json
# from fastapi.testclient import TestClient


def test_create_user(client):
    data = {
        "username": "testuser",
        "password": "testpassword",
        "first_name": "testuser_first_name",
        "last_name": "testuser_last_name"
    }
    response = client.post("/signup", json.dumps(data))
    print(response.text)
    assert response.status_code == 200
    # assert response.json()["id"]