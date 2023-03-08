from fastapi import Depends, APIRouter, status, HTTPException

from backend.crud.crud_user import UserCruds
from backend.crud.crud_tracks import TracksCrud
from backend.crud.crud_change_roles import ChangeRolesCruds
from backend.helpers.auth_helper import Authenticate
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.schemas.statistics import TrackStats, UsersStats
from backend.core.config import settings
import uuid as uuid_pkg
router = APIRouter(tags=['Статистика'], prefix='/statistics')


@router.get('', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UsersStats)
def get_users_count(Auth: Authenticate = Depends(Authenticate(is_admin=True))):
    '''Получение статистики по пользователям'''
    users_crud = UserCruds(db=Auth.db)
    user_count = users_crud.get_count()
    admin_count = users_crud.get_count_by_type(settings.UserTypeEnum.superuser)
    musician_count = users_crud.get_count_by_type(
        settings.UserTypeEnum.musician)
    change_role_request_count = ChangeRolesCruds(
        db=Auth.db).get_not_answered_change_role_request_count()
    return UsersStats(
        user_count=user_count,
        admin_count=admin_count,
        change_role_request_count=change_role_request_count,
        musician_count=musician_count
    )


@router.get('/track/{track_id}', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=TrackStats)
def get_track_statistics(track_id: uuid_pkg.UUID, Auth: Authenticate = Depends(Authenticate(is_admin=True, is_musician=True))):
    '''Получение статистики по треку'''

    tracks_crud = TracksCrud(db=Auth.db)
    track = tracks_crud.get_track(track_id=track_id)
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Трек не найден'
        )
    users_cruds = UserCruds(db=Auth.db)
    db_public_profile = users_cruds.get_public_profile_by_id(
        Auth.current_user_id)
    if not (Auth.current_user.type == settings.UserTypeEnum.superuser) and not (db_public_profile or db_public_profile.id != track.artist_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас нет доступа к этой информации'
        )

    return tracks_crud.get_track_statistics(track=track)
