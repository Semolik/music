# from fastapi.testclient import TestClient
# from backend.core.config import settings
# from backend.crud.crud_user import UserCruds
# from tests.utils.roles import send_change_role_request


# def test_send_change_role_request(client: TestClient, normal_user_token_cookies):

#     response = send_change_role_request(
#         client=client, cookies=normal_user_token_cookies)
#     assert response.status_code == 200


# def test_change_role_requests_limit(client: TestClient, normal_user_token_cookies):

#     requests = [send_change_role_request(
#         client=client, cookies=normal_user_token_cookies) for _ in range(5)]
#     assert set([r.status_code for r in requests][0: -1][0:-1]) == {200}
#     assert requests[-1].status_code == 403


# def test_get_all_change_role_requests(client: TestClient, normal_admin_token_cookies):
#     response = client.get('change-role-requests',
#                           cookies=normal_admin_token_cookies, params={'filter': 'all', 'page': 1})
#     assert response.status_code == 200


# # def test_send_change_role_request_answer(client: TestClient, normal_admin_token_cookies, db_session):
# #     db_user = UserCruds(db_session).get_user_by_username(
# #         username=settings.TEST_uSER_USERNAME)
# #     #
