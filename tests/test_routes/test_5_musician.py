import json
from fastapi.testclient import TestClient
musician_id = 1


def test_get_musician_profile(client: TestClient):
    response = client.get(
        f"/musician/{musician_id}")
    assert response.status_code == 200


def test_like_musician(client: TestClient, normal_user_token_cookies):
    response = client.put(
        f"/musician/{musician_id}/like", cookies=normal_user_token_cookies)
    assert response.json() == True
    assert response.status_code == 200


def test_unlike_musician(client: TestClient, normal_user_2_token_cookies):
    response = client.put(
        f"/musician/{musician_id}/like", cookies=normal_user_2_token_cookies)
    assert response.status_code == 200
    assert response.json() == False
