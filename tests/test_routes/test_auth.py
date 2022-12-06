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
    # print(response.headers['set-cookie'])
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
    print(cookies)
    response = client.put("/me", data=data, cookies=cookies)
    print(response.text)
    assert response.status_code == 201
