from fastapi.testclient import TestClient


def send_change_role_request(client: TestClient, cookies, message='test message', account_status='musician'):
    data = {
        'message': message,
        'account_status': account_status,
    }
    filename = 'tests/assets/test-profile-avatar.jpg'
    files = {'files': ('filename.jpg', open(filename, 'rb'), 'image/jpeg')}

    response = client.post(
        "/change-role", data=data, cookies=cookies, files=files)
    return response
