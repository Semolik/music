import io
from fastapi.testclient import TestClient
from backend.crud.crud_genres import GenresCruds
from backend.helpers.images import save_image

baseGenreData = {
    "data": {

        "name": "test_genre_name",

    },
    "files": {
        "genrePicture": open("tests/assets/test-profile-avatar.jpg", "rb"),
    }
}


def test_create_genre(client: TestClient, normal_admin_token_cookies):

    response = client.post(
        "/genres",
        data=baseGenreData.get("data"),
        cookies=normal_admin_token_cookies,
        files=baseGenreData.get("files")
    )
    assert response.status_code == 200
    assert response.json()["name"] == baseGenreData.get("data")["name"]


def test_get_genre(client: TestClient):
    response = client.get(
        "/genres/1")
    assert response.status_code == 200


def test_get_genres(client: TestClient):
    response = client.get(
        "/genres")
    assert response.status_code == 200


def test_update_genre(client: TestClient, normal_admin_token_cookies):
    newGenreData = {
        "name": "test_genre_name_updated"
    }
    response = client.put(
        "/genres/1",
        data=newGenreData,
        cookies=normal_admin_token_cookies,
        files=baseGenreData.get("files")
    )
    assert response.status_code == 200
    assert response.json()["name"] == newGenreData["name"]


def test_delete_genre(client: TestClient, normal_admin_token_cookies, db_session):
    admin_id = client.get("/users/me").json()["id"]
    genres_crud = GenresCruds(db_session)
    img = io.BytesIO(open("tests/assets/test-profile-avatar.jpg", "rb").read())
    img.name = "test-profile-avatar.jpg"

    image = save_image(
        db=db_session,
        user_id=admin_id,
        upload_file=None,
        bytes_io_file=img
    )
    genre = genres_crud.create_genre(
        name="test_genre_name_to_delete",
        picture=image
    )
    response = client.delete(
        f"/genres/{genre.id}",
        cookies=normal_admin_token_cookies
    )
    assert response.status_code == 204


def test_delete_genre_not_found(client: TestClient, normal_admin_token_cookies):
    response = client.delete(
        "/genres/10000",
        cookies=normal_admin_token_cookies
    )
    assert response.status_code == 404


def test_delete_genre_not_admin(client: TestClient, normal_user_token_cookies):
    response = client.delete(
        "/genres/1",
        cookies=normal_user_token_cookies
    )
    assert response.status_code == 403


def test_update_genre_not_found(client: TestClient, normal_admin_token_cookies):
    response = client.put(
        "/genres/10000",
        data=baseGenreData.get("data"),
        cookies=normal_admin_token_cookies,
        files=baseGenreData.get("files")
    )
    assert response.status_code == 404


def test_update_genre_not_admin(client: TestClient, normal_user_token_cookies):
    response = client.put(
        "/genres/1",
        data=baseGenreData.get("data"),
        cookies=normal_user_token_cookies,
        files=baseGenreData.get("files")
    )
    assert response.status_code == 403


def test_get_genre_not_found(client: TestClient):
    response = client.get(
        "/genres/10000")
    assert response.status_code == 404


def test_create_genre_not_admin(client: TestClient, normal_user_token_cookies):
    response = client.post(
        "/genres",
        data=baseGenreData.get("data"),
        cookies=normal_user_token_cookies,
        files=baseGenreData.get("files")
    )
    assert response.status_code == 403
