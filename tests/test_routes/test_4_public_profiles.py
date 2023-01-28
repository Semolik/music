from fastapi.testclient import TestClient
data = {
    'name': 'test_name',
    # 'surname': 'test_surname',
    'description': 'test_description',
    'links': {
        'youtube': 'test_youtube',
        'vk': 'test_vk',
        'telegram': 'test_telegram',
    }
}
picture = open('tests/assets/test-profile-avatar.jpg', 'rb')


def test_get_my_public_profile(client: TestClient, normal_user_token_cookies):

    response = client.get("/users/me/public",
                          cookies=normal_user_token_cookies)
    print(response.json())
    assert response.status_code == 200
