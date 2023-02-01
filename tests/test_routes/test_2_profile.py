import json
import pytest

from fastapi.testclient import TestClient
files = {'userPicture':  open(
    'tests/test_files/test-profile-avatar.jpg', 'rb')}
data = {
    "name": "new_test_name",
    "description": "new_test_last_name",
    "remove_picture": False,
    "vk": "https://vk.com/id123456789",
    "telegram": "https://telegram.com/user123456789",
    "youtube": "https://youtube.com/user123456789",
}


def test_get_user_info(client: TestClient, normal_user_token_cookies):
    response = client.get("/users/me", cookies=normal_user_token_cookies)

    assert response.status_code == 200


@pytest.mark.parametrize("data, files, status_code", [
    (data, files, 200),
    (data, {
        'userPicture':  b'broken picture'
    }, 422),
    ({**data, "remove_picture": True}, {}, 200),
    ({**data, "remove_picture": True}, files, 200),
])
def test_update_user_info(client: TestClient, normal_user_token_cookies, data, files, status_code):
    response = client.put(
        "/users/me",
        data={"UserData": json.dumps(data)},
        files=files,
        cookies=normal_user_token_cookies
    )
    assert response.status_code == status_code
