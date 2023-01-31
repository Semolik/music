from typing import List
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi_jwt_auth import AuthJWT

from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCruds
from backend.crud.crud_tracks import TracksCrud
from backend.crud.crud_change_roles import ChangeRolesCruds
from backend.helpers.validate_role import validate_admin
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.schemas.statistics import UsersStats
router = APIRouter(tags=['Статистика'], prefix='/statistics')


@router.get('', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UsersStats)
def get_users_count(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    '''Получение статистики по пользователям'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_admin(db=db, user_id=current_user_id)
    user_count = UserCruds(db=db).get_count()
    admin_count = UserCruds(db=db).get_count_by_type('superuser')
    musician_count = UserCruds(db=db).get_count_by_type('musician')
    change_role_request_count = ChangeRolesCruds(
        db=db).get_not_answered_change_role_request_count()
    return UsersStats(
        user_count=user_count,
        admin_count=admin_count,
        change_role_request_count=change_role_request_count,
        musician_count=musician_count
    )


@router.get('/track/{track_id}', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def get_track_statistics(track_id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    '''Получение статистики по треку'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    track = TracksCrud(db=db).get_track(track_id=track_id)
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Трек не найден'
        )
    users_cruds = UserCruds(db=db)
    db_public_profile = users_cruds.get_public_profile_by_id(current_user_id)
    if not users_cruds.is_admin(current_user_id) and (not db_public_profile or db_public_profile.id != track.artist_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас нет доступа к этой информации'
        )
    return TracksCrud(db=db).get_track_statistics(track_id=track_id)
