import io
import json
from fastapi.testclient import TestClient
from datetime import datetime
from backend.crud.crud_genres import GenresCruds
from backend.core.config import env_config
import pytest

data = {

    "albumData": json.dumps({
        "name": "string",
        "date": str(datetime.now()),
        "genres_ids": []
    })

}
files = {
    "albumPicture": (open("tests/assets/album_picture.jpg", "rb"))
}

track_files = {
    "track": (open("tests/assets/track.mp3", "rb")),
    "trackPicture": (open("tests/assets/track_picture.jpg", "rb"))
}
# track_data =


def test_create_album(client: TestClient, normal_musician_token_cookies, db_session):
    genres_crud = GenresCruds(db_session)
    genres_ids = [genre.id for genre in genres_crud.get_genres()]
    data["genres_ids"] = genres_ids
    response = client.post("/albums", data=data, files=files,
                           cookies=normal_musician_token_cookies)
    json_resp = response.json()
    print(json_resp)
    global album_id
    assert response.status_code == 201
    # assert json_resp.get("name") == data["albumData"]["name"]
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
