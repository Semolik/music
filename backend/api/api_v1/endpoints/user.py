from sqlalchemy.orm import Session
from backend.models.user import User as UserModel
from backend.core.config import settings
from backend.db.db import get_db
from backend.crud.crud_user import UserCruds
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.schemas.user import PublicProfile, PublicProfileModifiable, UserInfo, UserModifiable
from backend.schemas.playlists import PlaylistInfoWithoutTracks, order_playlist_by
from backend.helpers.images import save_image
from backend.helpers.auth_helper import Authenticate
from backend.crud.crud_playlists import PlaylistsCrud
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, APIRouter, HTTPException, Query, status, UploadFile, File
from typing import List, Literal

router = APIRouter(tags=['Профили пользователей'], prefix='/users')


@router.put('/me',  response_model=UserInfo)
def update_user_data(
    UserData: UserModifiable,
    Auth: Authenticate = Depends(Authenticate()),
    userPicture: UploadFile = File(
        default=False, description='Фото пользователя'),
):
    '''Обновление данных пользователя'''
    db_image = save_image(db=Auth.db, upload_file=userPicture,
                          user_id=Auth.current_user.id)
    db_user_updated = UserCruds(Auth.db).update_user(
        user=Auth.current_user,
        userPic=db_image,
        first_name=UserData.first_name,
        last_name=UserData.last_name,
        remove_picture=UserData.remove_picture
    )
    return db_user_updated


@router.get('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def get_user_info(Auth: Authenticate = Depends(Authenticate())):
    '''Получение данных пользователя'''
    return Auth.current_user


@router.put('/me/public', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=PublicProfile)
def update_user_public_profile_data(
    PublicProfileData: PublicProfileModifiable,
    userPublicPicture: UploadFile = File(
        default=False, description='Фото публичного профиля'),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Обновление данных публичного профиля пользователя'''
    user_cruds = UserCruds(Auth.db)
    db_public_profile = user_cruds.get_public_profile(
        user_id=Auth.current_user.id)
    db_image = save_image(
        db=Auth.db,
        upload_file=userPublicPicture,
        user_id=Auth.current_user.id
    )
    db_public_profile_updated = user_cruds.update_public_profile(
        public_profile=db_public_profile,
        name=PublicProfileData.name,
        description=PublicProfileData.description,
        vk_username=PublicProfileData.vk,
        youtube_channel_id=PublicProfileData.youtube,
        telegram_username=PublicProfileData.telegram,
        userPublicPicture=db_image,
        remove_picture=PublicProfileData.remove_picture
    )
    return db_public_profile_updated


@router.get('/me/public', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=PublicProfile)
def get_user_public_profile_info(
    Auth: Authenticate = Depends(Authenticate(is_musician=True))
):
    '''Получение данных публичного профиля пользователя'''
    return UserCruds(Auth.db).get_public_profile(user_id=Auth.current_user.id)


@router.get('/{user_id}/playlists', response_model=List[PlaylistInfoWithoutTracks])
def get_user_playlists(
    Auth: Authenticate = Depends(Authenticate(required=False)),
    user_id: int = Query(
        default=None, description='ID пользователя', required=True),
    order_by: order_playlist_by = Query(
        default='created_at', description='Порядок сортировки', required=True),
    order_orientation: Literal['asc', 'desc'] = Query(
        default='asc', description='Направление сортировки', required=True),
):
    '''Получение списка плейлистов'''

    db_requested_user = UserCruds(Auth.db).get_user_by_id(user_id=user_id)
    if not db_requested_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    playlists = PlaylistsCrud(Authenticate.db).get_playlists_by_user_id(
        user_id=Authenticate.current_user_id,
        owner_id=user_id,
        order_by=order_by,
        order_orientation=order_orientation
    )
    return playlists
