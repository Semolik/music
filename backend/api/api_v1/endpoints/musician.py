from typing import List
from fastapi import Depends, APIRouter, status, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_clips import ClipsCruds
from backend.crud.crud_musician import MusicianCrud
from backend.helpers.clips import set_clip_data
from backend.helpers.users import get_musician_profile_as_dict
from backend.schemas.music import Liked, MusicianClip
from backend.schemas.music import MusicianFullInfo
from backend.crud.crud_user import UserCruds
from backend.db.db import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix='/musician', tags=['Музыканты'])


@router.get('/{profile_id}', response_model=MusicianFullInfo)
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


@router.put('/{profile_id}/like', response_model=Liked)
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


@router.get('/{profile_id}/clips', response_model=List[MusicianClip])
def get_musician_clips(
    musician_id: int = Query(..., description='ID музыканта'),
    page: int = Query(1, description='Страница'),
    db: Session = Depends(get_db)
):
    '''Получение клипов музыканта'''
    db_public_profile = UserCruds(db).get_public_profile_by_id(id=musician_id)
    if not db_public_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    clips = ClipsCruds(db).get_musician_clips(
        musician_id=db_public_profile.id, page=page)
    return [set_clip_data(clip=clip) for clip in clips]
