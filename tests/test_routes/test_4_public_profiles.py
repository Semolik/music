import json
from fastapi.testclient import TestClient
data = {
    'name': 'test_name',
    'description': 'test_description',
    'links': {
        'youtube': 'test_youtube',
        'vk': 'test_vk',
        'telegram': 'test_telegram',
    }
}
picture = open('tests/test_files/test-profile-avatar.jpg', 'rb')


def test_get_my_public_profile(client: TestClient, normal_user_token_cookies):
    response = client.get("/users/me/public",
                          cookies=normal_user_token_cookies)
    assert response.status_code == 200


def test_update_my_public_profile(client: TestClient, normal_user_token_cookies):
    data = {
        "youtube": "string",
        "telegram": "string",
        "vk": "string",
        "name": "string",
        "description": "string",
        "remove_picture": False,
    }
    response = client.put(
        "/users/me/public",
        cookies=normal_user_token_cookies, data={
            "PublicProfileData": json.dumps(data)},
        files={'userPublicPicture': picture})
    assert response.status_code == 200


def test_remove_my_public_profile_picture(client: TestClient, normal_user_token_cookies):
    data = {
        "youtube": "string",
        "telegram": "string",
        "vk": "string",
        "name": "string",
        "description": "string",
        "remove_picture": True,
    }
    response = client.put(
        "/users/me/public",
        cookies=normal_user_token_cookies, data={
            "PublicProfileData": json.dumps(data)})
    assert response.status_code == 200
