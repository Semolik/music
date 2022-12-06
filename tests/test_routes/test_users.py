import json


def test_create_user(client):

    response = client.get("/")

    data = {
        "username": "testuser",
        "password": "testpassword",
        "first_name": "test_name",
        "last_name": "test_last_name"
    }
    response = client.post("/signup", json.dumps(data))
    print(response.text)
    assert response.status_code == 201
    # assert response.json()["id"]
