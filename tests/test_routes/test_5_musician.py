
import random
from fastapi.testclient import TestClient


def test_like_musicians(client: TestClient, normal_user_token_cookies, normal_musicians_tokens_cookies):
    musicians = [
        client.get('/users/me/public', cookies=cookies).json() for cookies in normal_musicians_tokens_cookies
    ]
    print(musicians)
    count = random.randint(1, len(normal_musicians_tokens_cookies))
    for musician in random.sample(musicians, count):
        response = client.put(
            f"/musician/{musician['id']}/like", cookies=normal_user_token_cookies)
        assert response.json() == True
        assert response.status_code == 200
    liked_musicians = client.get(
        '/musician/liked', cookies=normal_user_token_cookies).json()
    assert len(liked_musicians) == count
