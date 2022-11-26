from fastapi import Depends, APIRouter, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_music import music_crud
from backend.helpers.users import get_public_profile_as_dict
from backend.schemas.track import Liked
from backend.schemas.user import MusicianFullInfo
from backend.crud.crud_user import user_cruds
router = APIRouter(prefix='/musician', tags=['Музыканты'])


@router.get('/',  response_model=MusicianFullInfo)
def get_public_profile_info(profile_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    current_user_id = Authorize.get_jwt_subject()
    public_profile_obj = get_public_profile_as_dict(
        public_profile_id=profile_id, full_links=True, liked_user_id=current_user_id)
    if not public_profile_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    return public_profile_obj


@router.post('/like', response_model=Liked)
def like_musician(profile_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not user_cruds.get_public_profile_by_id(id=profile_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    liked = music_crud.toggle_like_musician(
        musician_id=profile_id, user_id=current_user_id)
    return Liked(liked=liked)
