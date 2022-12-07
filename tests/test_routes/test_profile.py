from fastapi.testclient import TestClient


def test_update_user_info(client: TestClient, normal_user_token_cookies):

    data = {
        "first_name": "",
        "last_name": "test_last_name",
        "remove_picture": False
    }
    files = {'userPicture':  open(
        'tests/assets/test-profile-avatar.jpg', 'rb')}
    response = client.put(
        "/me", data=data, files=files, cookies=normal_user_token_cookies)
    assert response.status_code == 200
