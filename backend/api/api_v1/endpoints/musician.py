from fastapi import Depends, APIRouter, status, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_musician import MusicianCrud
from backend.helpers.users import get_musician_profile_as_dict
from backend.schemas.music import Liked
from backend.schemas.music import MusicianFullInfo
from backend.crud.crud_user import UserCruds
from backend.db.db import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix='/musician', tags=['Музыканты'])


@router.get('/', response_model=MusicianFullInfo)
def get_public_profile_info(
        profile_id: int = Query(..., description='ID профиля'),
        Authorize: AuthJWT = Depends(),
        db: Session = Depends(get_db)
):
    '''Получение информации о публичном профиле музыканта'''
    Authorize.jwt_optional()
    current_user_id = Authorize.get_jwt_subject()
    public_profile_obj = get_musician_profile_as_dict(
        db=db,
        public_profile_id=profile_id,
        full_links=True,
        user_id=current_user_id
    )
    if not public_profile_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    return public_profile_obj


@router.post('/like', response_model=Liked)
def like_musician(
    profile_id: int = Query(..., description='ID профиля'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Лайк музыканта'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not UserCruds(db).get_public_profile_by_id(id=profile_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    liked = MusicianCrud(db).toggle_like_musician(
        musician_id=profile_id, user_id=current_user_id)
    return Liked(liked=liked)
