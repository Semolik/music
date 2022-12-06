import json
from fastapi.testclient import TestClient


def test_update_user_info(client: TestClient):

    data = {
        "first_name": "test_name",
        "last_name": "test_last_name"
    }
    response = client.put("/me", data=data)
    assert response.status_code == 201
