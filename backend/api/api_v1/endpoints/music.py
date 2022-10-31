from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.schemas.track import UploadTrack
from backend.helpers.files import save_file

from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.crud.crud_user import user_cruds
router = APIRouter(tags=['Треки'])


@router.post('/upload_song', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def update_user_data(trackData: UploadTrack, trackPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    if not db_user.is_musician:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="необходим статус музыкант")
    db_image = save_file(upload_file=trackPicture,
                         user_id=db_user.id, force_image=True)
