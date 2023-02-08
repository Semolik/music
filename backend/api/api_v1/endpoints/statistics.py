from fastapi import Depends, APIRouter, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.crud.crud_user import UserCruds
from backend.crud.crud_tracks import TracksCrud
from backend.crud.crud_change_roles import ChangeRolesCruds
from backend.helpers.auth_helper import validate_authorized_user
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.schemas.statistics import UsersStats
from backend.core.config import settings
import uuid as uuid_pkg
router = APIRouter(tags=['Статистика'], prefix='/statistics')


@router.get('', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UsersStats)
def get_users_count(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    '''Получение статистики по пользователям'''
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_authorized_user(
        Authorize=Authorize, db=db,
        types=[settings.UserTypeEnum.superuser]
    )
    users_crud = UserCruds(db=db)
    user_count = users_crud.get_count()
    admin_count = users_crud.get_count_by_type(settings.UserTypeEnum.superuser)
    musician_count = users_crud.get_count_by_type(
        settings.UserTypeEnum.musician)
    change_role_request_count = ChangeRolesCruds(
        db=db).get_not_answered_change_role_request_count()
    return UsersStats(
        user_count=user_count,
        admin_count=admin_count,
        change_role_request_count=change_role_request_count,
        musician_count=musician_count
    )


@router.get('/track/{track_id}', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def get_track_statistics(track_id: uuid_pkg.UUID, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    '''Получение статистики по треку'''
    Authorize.jwt_required()
    tracks_crud = TracksCrud(db=db)
    track = tracks_crud.get_track(track_id=track_id)
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Трек не найден'
        )
    users_cruds = UserCruds(db=db)
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db,
        types=[settings.UserTypeEnum.musician, settings.UserTypeEnum.superuser]
    )
    db_public_profile = users_cruds.get_public_profile_by_id(db_user.id)
    if not (db_user.type == settings.UserTypeEnum.superuser) and not (db_public_profile or db_public_profile.id != track.artist_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас нет доступа к этой информации'
        )

    return tracks_crud.get_track_statistics(track=track)
