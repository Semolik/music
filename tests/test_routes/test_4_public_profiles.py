import json
import pytest
from fastapi.testclient import TestClient
from backend.core.config import env_config
data = {
    'name': 'test_name',
    'description': 'test_description',
    'youtube': 'test',
    'telegram': 'test',
    'vk': 'example_username',

}
picture = open('tests/test_files/test-profile-avatar.jpg', 'rb')


def test_get_my_public_profile(client: TestClient, normal_user_token_cookies):
    response = client.get("/users/me/public",
                          cookies=normal_user_token_cookies)
    assert response.status_code == 200


@pytest.mark.parametrize("data, files, status_code", [
    (data, {'userPublicPicture': picture}, 200),
    (data, {'userPublicPicture': b'broken picture'}, 422),
    ({**data, "remove_picture": True}, {}, 200),
    ({**data, "description": int(env_config.get("VITE_MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH"))*"a"}, {}, 200),
    ({**data, "description": int(env_config.get("VITE_MAX_PUBLIC_PROFILE_DESCRIPTION_LENGTH"))*"a" + "a"}, {}, 422),
    ({**data, "name": int(env_config.get("VITE_MAX_PUBLIC_PROFILE_NAME_LENGTH"))*"a"}, {}, 200),
    ({**data, "name": (int(env_config.get("VITE_MAX_PUBLIC_PROFILE_NAME_LENGTH"))+3)*"a"}, {}, 422),
    ({**data, "name": ""}, {}, 422),
    ({**data, "description": ""}, {}, 200),
    ({**data, "vk": "id123456789"}, {}, 200),
    ({**data, "youtube": "asdasdasda"}, {}, 200),
    ({**data, "telegram": "user123456789"}, {}, 200),
    ({**data, "vk": "rfsdfsdf", "youtube": "asdasd",
     "telegram": "asdasdas"}, {}, 200),
    ({**data, "vk": "", "youtube": "", "telegram": ""}, {}, 200),
])
def test_update_my_public_profile(client: TestClient, normal_musician_token_cookies, data, files, status_code):
    response = client.put(
        "/users/me/public",
        cookies=normal_musician_token_cookies, data={
            "PublicProfileData": json.dumps(data)},
        files=files)

    assert response.status_code == status_code
