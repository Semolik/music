from fastapi.testclient import TestClient
from backend.models.roles import ChangeRoleRequestStatus
from tests.utils.roles import send_change_role_request
import pytest
from backend.models.roles import ChangeRoleRequestStatus


def test_send_change_role_request(client: TestClient, normal_user_token_cookies):

    response = send_change_role_request(
        client=client, cookies=normal_user_token_cookies)

    assert response.status_code == 201


def test_change_role_requests_limit(client: TestClient, normal_user_token_cookies):

    requests = [send_change_role_request(
        client=client, cookies=normal_user_token_cookies) for _ in range(4)]
    assert set([r.status_code for r in requests][0: -1][0:-1]) == {201}
    assert requests[-1].status_code == 403


def test_get_all_change_role_requests(client: TestClient, normal_admin_token_cookies):
    response = client.get('change-role/all',
                          cookies=normal_admin_token_cookies, params={'page': 1})
    print(response.json())
    global change_role_requests
    change_role_requests = response.json()

    assert response.status_code == 200


@pytest.mark.parametrize("filter", [i.value for i in ChangeRoleRequestStatus])
def test_get_all_change_role_requests_with_filter(client: TestClient, normal_admin_token_cookies, filter):
    response = client.get('change-role/all',
                          cookies=normal_admin_token_cookies, params={'page': 1, 'filter': filter})
    assert response.status_code == 200


def test_send_change_role_request_answer(client: TestClient, normal_admin_token_cookies):

    response = client.post(
        f"change-role/{change_role_requests[0]['id']}/answer",
        cookies=normal_admin_token_cookies,
        json={
            "message": "ok i accept your request",
            "setted_account_status": change_role_requests[0].get('requested_account_status'),
            "request_status": ChangeRoleRequestStatus.accepted.value
        }
    )
    assert response.status_code == 200
