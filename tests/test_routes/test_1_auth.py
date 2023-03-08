import json
import pytest

from fastapi.testclient import TestClient
from backend.core.config import env_config, settings
from tests.utils.names import generate_random_name

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


def test_logout(client: TestClient):
    response = client.delete("/auth/logout", cookies=cookies)
    assert response.status_code == 200


def test_get_refresh_token(client: TestClient):
    response = client.post("/auth/refresh", cookies=cookies)
    assert response.status_code == 204


@pytest.mark.parametrize("username_length,expected_status_code", [
    (int(env_config.get("VITE_MAX_LOGIN_LENGTH")), 201),
    (int(env_config.get("VITE_MAX_LOGIN_LENGTH")) + 1, 422),
    (int(env_config.get("VITE_MIN_LOGIN_LENGTH")) - 1, 422),
    (int(env_config.get("VITE_MIN_LOGIN_LENGTH")), 201),
])
def test_create_user_with_wrong_username_length(client: TestClient, username_length, expected_status_code):
    response = client.post(
        "/auth/signup", json={**data, "username": generate_random_name(username_length)})

    assert response.status_code == expected_status_code


@pytest.mark.parametrize("password_length,expected_status_code", [

    (int(env_config.get("VITE_MAX_PASSWORD_LENGTH")), 201),
    (int(env_config.get("VITE_MAX_PASSWORD_LENGTH")) + 1, 422),
    (int(env_config.get("VITE_MIN_PASSWORD_LENGTH")) - 1, 422),
    (int(env_config.get("VITE_MIN_PASSWORD_LENGTH")), 201),
])
def test_create_user_with_wrong_password_length(client: TestClient, password_length, expected_status_code):
    response = client.post(
        "/auth/signup", json={**data, "password": generate_random_name(password_length), "username": generate_random_name(10)})
    assert response.status_code == expected_status_code
