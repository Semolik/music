from fastapi import Depends, APIRouter, status, UploadFile, File
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_music import music_crud
from backend.helpers.validate_role import validate_musician
from backend.responses import NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.track import CreateAlbumForm, UploadTrack
from backend.helpers.files import save_file
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.crud.crud_user import user_cruds
router = APIRouter(tags=['Музыка'])


@router.post('/create_album', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER})
def update_user_data(albumData: CreateAlbumForm = Depends(CreateAlbumForm), albumPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    db_image = save_file(upload_file=albumPicture,
                         user_id=db_user.id, force_image=True)
    db_album = music_crud.create_album(
        name=albumData.name, musician_id=current_user_id, date=albumData.date, picture=db_image)
    return db_album.as_dict()


@router.post('/upload_song', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER})
def update_user_data(trackData: UploadTrack, trackPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    db_image = save_file(upload_file=trackPicture,
                         user_id=db_user.id, force_image=True)
