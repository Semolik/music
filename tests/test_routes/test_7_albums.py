import json
from fastapi.testclient import TestClient
from datetime import datetime
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_genres import GenresCruds
from backend.core.config import env_config
import pytest
json_data = {
    "name": "string",
    "date": str(datetime.now()),
    "genres_ids": []
}
data = {

    "albumData": json.dumps(json_data)

}
update_json_data = json_data.copy()
update_json_data["name"] = "new_name"
files = {
    "albumPicture": ("test_albums_picture.jpg", open("tests/test_files/album_picture.jpg", "rb"), "image/jpg")
}

track_files = {
    "track": open("tests/test_files/track.mp3", "rb"),
    "trackPicture": open("tests/test_files/test_tracks_picture.jpg", "rb")
}
track_ids = []


def test_create_album(client: TestClient, normal_musician_token_cookies, db_session):
    genres_crud = GenresCruds(db_session)
    genres_ids = [genre.id for genre in genres_crud.get_genres()]
    data["genres_ids"] = genres_ids
    response = client.post("/albums", data=data, files=files,
                           cookies=normal_musician_token_cookies)
    json_resp = response.json()
    global album_id
    assert response.status_code == 201
    album_id = json_resp.get("id")


@pytest.mark.parametrize("input_data,files,expected_status_code", [
    ({
        "name": "test_track_name",
        "feat": "test_track_feat",
    }, track_files, 201),
    ({
        "name": "",
        "feat": "test_track_feat",
    }, track_files, 422),
    ({
        "name": (int(env_config.get("VITE_MAX_TRACK_NAME_LENGTH"))+1)*"a",
        "feat": "",
    }, track_files, 422),
    (
        {
            "name": "test_track_name",
            "feat": "feat",
        },
        {
            "track": b'aboba',
            "trackPicture": track_files["trackPicture"]
        },
        422
    ),
    (
        {
            "name": "test_track_name",
            "feat": "feat",
        },
        {
            "track": track_files["track"],
            "trackPicture": b'aboba'
        },
        422
    ),
])
def test_upload_track(client: TestClient, normal_musician_token_cookies, expected_status_code: int, input_data: dict, files):
    assert album_id is not None
    response = client.post(f"/albums/{album_id}/track", data=input_data, files=files,
                           cookies=normal_musician_token_cookies)
    print(response.json())
    assert response.status_code == expected_status_code
    if response.status_code == 201:
        track_ids.append(response.json().get("id"))


def test_upload_track_as_another_musician(client: TestClient, another_normal_musician_token_cookies):
    assert album_id is not None
    response = client.post(f"/albums/{album_id}/track", data={
        "name": "test_track_name",
        "feat": "feat",
    }, files=track_files, cookies=another_normal_musician_token_cookies)

    assert response.status_code == 403


def test_upload_track_without_album(client: TestClient, normal_musician_token_cookies):
    response = client.post(f"/albums/0/track", data={
        "name": "test_track_name",
        "feat": "feat",
    }, files=track_files, cookies=normal_musician_token_cookies)

    assert response.status_code == 404


def test_upload_multiple_tracks(client: TestClient, normal_musician_token_cookies):
    for i in range(5):
        test_upload_track(client=client, normal_musician_token_cookies=normal_musician_token_cookies, input_data={
            "name": "test_track_name",
            "feat": "test_track_feat",
        }, files={
            "track": track_files["track"],
            "trackPicture": open("tests/test_files/test_tracks_picture.jpg", "rb")
        }, expected_status_code=201)
        print(i)


def test_get_album_with_not_closed_uploading_as_user(client: TestClient, normal_user_token_cookies):
    assert album_id is not None
    response = client.get(
        f"/albums/{album_id}", cookies=normal_user_token_cookies)

    assert response.status_code == 404


def test_get_album_with_not_closed_uploading_as_musician(client: TestClient, normal_musician_token_cookies):
    assert album_id is not None
    response = client.get(
        f"/albums/{album_id}", cookies=normal_musician_token_cookies)

    assert response.status_code == 404


def test_get_track_from_album_with_not_closed_uploading_as_user(client: TestClient, normal_user_token_cookies):
    assert album_id is not None
    assert track_ids[0] is not None
    response = client.get(
        f"/tracks/{track_ids[0]}", cookies=normal_user_token_cookies)
    assert response.status_code == 404


def test_close_uploading(client: TestClient, normal_musician_token_cookies):
    assert album_id is not None
    response = client.put(
        f"/albums/{album_id}/close-uploading", cookies=normal_musician_token_cookies)

    assert response.status_code == 200


def test_get_album_with_closed_uploading_as_user(client: TestClient, normal_user_token_cookies):
    assert album_id is not None
    response = client.get(
        f"/albums/{album_id}", cookies=normal_user_token_cookies)

    assert response.status_code == 200


album_tracks_ids = []
update_json_data_change_tracks_position = update_json_data.copy()


def test_get_album_with_closed_uploading_as_musician(client: TestClient, normal_musician_token_cookies):
    assert album_id is not None
    response = client.get(
        f"/albums/{album_id}", cookies=normal_musician_token_cookies)

    assert response.status_code == 200


def test_set_tracks_ids_for_update(db_session):
    album_tracks_ids = [str(i.id) for i in
                        AlbumsCruds(db_session).get_album(album_id).tracks
                        ]

    update_json_data["tracks_ids"] = album_tracks_ids

    update_json_data_change_tracks_position["tracks_ids"] = list(
        reversed(album_tracks_ids))


@pytest.mark.parametrize("input_data,files,expected_status_code", [
    (update_json_data, files, 200),
    (update_json_data, {}, 200),
    (update_json_data, {
        "albumPicture": b'aboba'
    }, 422),
    (update_json_data, files, 200),
    (update_json_data_change_tracks_position, files, 200)
])
def test_update_album(client: TestClient, normal_musician_token_cookies, files, expected_status_code: int, input_data: dict):

    assert album_id is not None
    response = client.put(
        f"/albums/{album_id}", cookies=normal_musician_token_cookies, data={"albumData": json.dumps(input_data)}, files=files)
    print(response.json())
    assert response.status_code == expected_status_code
    if response.status_code == 200:
        assert response.json().get("name") == update_json_data["name"]


def test_update_album_without_album(client: TestClient, normal_musician_token_cookies):
    response = client.put(
        f"/albums/0", cookies=normal_musician_token_cookies, data={"albumData": json.dumps(update_json_data)})

    assert response.status_code == 404


def test_update_album_as_another_musician(client: TestClient, another_normal_musician_token_cookies):
    assert album_id is not None
    response = client.put(
        f"/albums/{album_id}", cookies=another_normal_musician_token_cookies, data={"albumData": json.dumps(update_json_data)})

    assert response.status_code == 403


def test_get_my_albums_as_musician(client: TestClient, normal_musician_token_cookies):
    response = client.get("/albums/my", cookies=normal_musician_token_cookies)
    assert response.status_code == 200


def test_get_my_albums_as_user(client: TestClient, normal_user_2_token_cookies):
    response = client.get("/albums/my", cookies=normal_user_2_token_cookies)
    assert response.status_code == 403


def test_album_like(client: TestClient, normal_user_token_cookies):
    assert album_id is not None
    response = client.put(
        f"/albums/{album_id}/like", cookies=normal_user_token_cookies)

    assert response.status_code == 200
