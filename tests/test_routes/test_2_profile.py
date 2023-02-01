import json
from fastapi.testclient import TestClient


def test_get_user_info(client: TestClient, normal_user_token_cookies):
    response = client.get("/users/me", cookies=normal_user_token_cookies)

    assert response.status_code == 200


def test_update_user_info_with_picture(client: TestClient, normal_user_token_cookies):

    data = {
        "first_name": "new_test_name",
        "last_name": "new_test_last_name",
        "remove_picture": False
    }
    files = {'userPicture':  open(
        'tests/test_files/test-profile-avatar.jpg', 'rb')}
    response = client.put(
        "/users/me",
        data={"UserData": json.dumps(data)},
        files=files,
        cookies=normal_user_token_cookies
    )

    assert response.status_code == 200


def test_update_user_info_without_picture(client: TestClient, normal_user_token_cookies):

    data = {
        "first_name": "aboba",
        "last_name": "test_last_name",
        "remove_picture": True
    }
    response = client.put(
        "/users/me", data={"UserData": json.dumps(data)}, cookies=normal_user_token_cookies)
    assert response.status_code == 200
