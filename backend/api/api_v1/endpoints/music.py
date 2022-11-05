from fastapi import Depends, APIRouter,  UploadFile, File
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_music import music_crud
from backend.helpers.music import save_track
from backend.helpers.users import get_public_profile_as_dict
from backend.helpers.validate_role import validate_musician
from backend.responses import NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.track import AlbumAfterUpload, CreateAlbumForm, TrackAfterUpload, UploadTrackForm
from backend.helpers.files import save_file

router = APIRouter(tags=['Музыка'])


@router.post('/create_album', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=AlbumAfterUpload)
def create_album(albumData: CreateAlbumForm = Depends(CreateAlbumForm), albumPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    db_image = save_file(upload_file=albumPicture,
                         user_id=db_user.id, force_image=True)
    db_album = music_crud.create_album(
        name=albumData.name, musician_id=current_user_id, date=albumData.date, picture=db_image)
    db_album_obj = db_album.as_dict()
    db_album_obj['year'] = db_album.open_date.year
    db_album_obj['artist'] = get_public_profile_as_dict(
        user_id=current_user_id)
    return db_album_obj


@router.post('/upload_song', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER}, response_model=TrackAfterUpload)
def upload_song(trackData: UploadTrackForm = Depends(UploadTrackForm), trackPicture: UploadFile = File(default=False), track: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    db_image = save_file(upload_file=trackPicture,
                         user_id=db_user.id, force_image=True)
    db_track = save_track(
        upload_file=track, user_id=current_user_id, track=trackData, picture=db_image)
    return db_track.as_dict()


@router.post('/get_my_albums', responses={**UNAUTHORIZED_401})
def get_musician_albums(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    