from fastapi.testclient import TestClient
from tests.utils.roles import send_change_role_request


def test_send_change_role_request(client: TestClient, normal_user_token_cookies):

    response = send_change_role_request(
        client=client, cookies=normal_user_token_cookies)
    assert response.status_code == 200
    return response


def test_send_change_role_requests_limit(client: TestClient, normal_user_token_cookies):

    requests = [send_change_role_request(
        client=client, cookies=normal_user_token_cookies) for _ in range(5)]
    assert set([r.status_code for r in requests][0: -1][0:-1]) == {200}
    assert requests[-1].status_code == 403
