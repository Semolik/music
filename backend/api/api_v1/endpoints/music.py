from fastapi import Depends, APIRouter, status, UploadFile, File
from fastapi_jwt_auth import AuthJWT
from backend.helpers.validate_role import validate_musician
from backend.responses import NOT_FOUND_USER, UNAUTHORIZED_401
from backend.schemas.track import CreateAlbum, UploadTrack
from backend.helpers.files import save_file
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.crud.crud_user import user_cruds
router = APIRouter(tags=['Музыка'])


@router.post('/create_album', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER})
def update_user_data(albumData: CreateAlbum, albumPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)


@router.post('/upload_song', responses={**UNAUTHORIZED_401, **NOT_FOUND_USER})
def update_user_data(trackData: UploadTrack, trackPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = validate_musician(user_id=current_user_id)
    db_image = save_file(upload_file=trackPicture,
                         user_id=db_user.id, force_image=True)
