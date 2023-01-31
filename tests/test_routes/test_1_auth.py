import json
import pytest

from fastapi.testclient import TestClient

data = {
    "username": "testuser2",
    "password": "testpassword2",
    "first_name": "test_name2",
    "last_name": "test_last_name2"
}


@pytest.mark.parametrize("input_data,expected_status_code", [(data, 201), (data, 400)])
def test_create_user(client: TestClient, input_data: dict, expected_status_code: int):
    response = client.post("/auth/signup", data=json.dumps(input_data))
    global cookies
    assert response.status_code == expected_status_code
    if response.status_code == 201:
        cookies = response.cookies


# def test_logout(client: TestClient):
#     response = client.delete("/auth/logout", cookies=cookies)
#     assert response.status_code == 200


# def test_get_refresh_token(client: TestClient):
#     response = client.post("/auth/refresh", cookies=cookies)
#     assert response.status_code == 200


# def test_create_user_with_wrong_password_length(client: TestClient):
#     local_data = data.copy()
#     local_data["password"] = "test"
#     response = client.post("/auth/signup", json=data)
#     assert response.status_code == 400
