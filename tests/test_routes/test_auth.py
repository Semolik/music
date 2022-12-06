import json


def test_create_user(client):

    data = {
        "username": "testuser",
        "password": "testpassword",
        "first_name": "test_name",
        "last_name": "test_last_name"
    }
    response = client.post("/signup", json.dumps(data))
    assert response.status_code == 201
