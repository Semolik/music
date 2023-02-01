from fastapi.testclient import TestClient
from backend.core.config import env_config
from backend.crud.crud_clips import ClipsCruds
import pytest
baseClipData = {
    "data": {
        "name": "test_clip_name",
        "video_id": "dQw4w9WgXcQ",
        "image_from_youtube": False,
    },
    "files": {
        "clipPicture": ("test_clip_picture.jpg", open("tests/test_files/test_clip_picture.jpg", "rb"), "image/jpeg"),
    }
}
tests = [
    (baseClipData.get("data"), baseClipData.get("files"), 201),
    ({**baseClipData.get("data"), "name": ""}, baseClipData.get("files"), 422),
    ({**baseClipData.get("data"), "name": (int(env_config.get("VITE_MAX_CLIP_NAME_LENGTH"))+1)
     * "a"}, baseClipData.get("files"), 422),
    ({**baseClipData.get("data"), "video_id": ""}, baseClipData.get("files"), 422),
    ({**baseClipData.get("data"), "video_id": "dQw4w9WgXcQ",
     "image_from_youtube": True}, {}, 201),
    ({**baseClipData.get("data"), "video_id": "a"*11},
     baseClipData.get("files"), 404),
]

update_tests = []
for test in tests:
    if test[2] == 201:
        update_tests.append((test[0], test[1], 200))
    else:
        update_tests.append(test)
tests.append(
    ({**baseClipData.get("data"), "video_id": "dQw4w9WgXcQ"}, {}, 400))
update_tests.append(
    ({**baseClipData.get("data"), "video_id": "dQw4w9WgXcQ"}, {}, 200))


@pytest.mark.parametrize("input_data,files,expected_status_code", tests)
def test_create_clip(client: TestClient, normal_musician_token_cookies, input_data, files, expected_status_code):
    response = client.post("/clips", data=input_data, files=files,
                           cookies=normal_musician_token_cookies)
    print(response.json())
    json_resp = response.json()
    assert response.status_code == expected_status_code
    if response.status_code == 201:

        assert json_resp.get("name") == input_data.get("name")


def test_create_clip_2(client: TestClient, normal_musician_token_cookies):
    response = client.post("/clips", data=baseClipData.get("data"), files=baseClipData.get("files"),
                           cookies=normal_musician_token_cookies)
    json_resp = response.json()
    assert response.status_code == 201
    global clip_id
    clip_id = json_resp.get("id")
    assert json_resp.get("name") == baseClipData.get("data").get("name")


@pytest.mark.parametrize("input_data,files,expected_status_code", update_tests)
def test_update_clip(client: TestClient, normal_musician_token_cookies, input_data, files, expected_status_code):
    response = client.put(f"/clips/{clip_id}", data=input_data, files=files,
                          cookies=normal_musician_token_cookies)
    json_resp = response.json()
    assert response.status_code == expected_status_code
    if response.status_code == 200:
        assert json_resp.get("name") == input_data.get("name")


def test_update_clip_as_another_musician(client: TestClient, normal_musician_token_cookies, another_normal_musician_token_cookies):
    response = client.post("/clips", data=baseClipData.get("data"), files=baseClipData.get("files"),
                           cookies=normal_musician_token_cookies)
    json_resp = response.json()
    assert response.status_code == 201

    response = client.put(f"/clips/{json_resp.get('id')}", data=baseClipData.get("data"), files=baseClipData.get("files"),
                          cookies=another_normal_musician_token_cookies)
    assert response.status_code == 403


def test_delete_clip(client: TestClient, normal_musician_token_cookies):
    response = client.post("/clips", data=baseClipData.get("data"), files=baseClipData.get("files"),
                           cookies=normal_musician_token_cookies)
    json_resp = response.json()
    assert response.status_code == 201

    clip_id = json_resp.get("id")
    assert json_resp.get("name") == baseClipData.get("data").get("name")
    response = client.delete(f"/clips/{clip_id}",
                             cookies=normal_musician_token_cookies)
    assert response.status_code == 204


def test_delete_clip_as_user(client: TestClient, normal_user_token_cookies, normal_musician_token_cookies):
    response = client.post("/clips", data=baseClipData.get("data"), files=baseClipData.get("files"),
                           cookies=normal_musician_token_cookies)
    json_resp = response.json()
    assert response.status_code == 201

    clip_id = json_resp.get("id")
    assert json_resp.get("name") == baseClipData.get("data").get("name")
    response = client.delete(f"/clips/{clip_id}",
                             cookies=normal_user_token_cookies)
    assert response.status_code == 403
