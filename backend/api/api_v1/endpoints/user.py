from typing import List, Literal
from fastapi import Depends, APIRouter, HTTPException, Query, status, UploadFile, File
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_playlists import PlaylistsCrud
from backend.helpers.auth_helper import validate_authorized_user
from backend.helpers.images import save_image
from backend.schemas.playlists import PlaylistInfoWithoutTracks, order_playlist_by
from backend.schemas.user import PublicProfile, PublicProfileModifiable, UserInfo, UserModifiable
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.crud.crud_user import UserCruds
from backend.db.db import get_db
from backend.core.config import settings

from sqlalchemy.orm import Session
router = APIRouter(tags=['Профили пользователей'], prefix='/users')


@router.put('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def update_user_data(
        UserData: UserModifiable,
        userPicture: UploadFile = File(
            default=False, description='Фото пользователя'),
        Authorize: AuthJWT = Depends(),
        db: Session = Depends(get_db)
):
    '''Обновление данных пользователя'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(Authorize, db)
    db_image = save_image(db=db, upload_file=userPicture,
                          user_id=db_user.id)
    db_user_updated = UserCruds(db).update_user(
        user=db_user, new_user_data=UserData, userPic=db_image)
    return db_user_updated


@router.get('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def get_user_info(Authorize: AuthJWT = Depends(),
                  db: Session = Depends(get_db)):
    '''Получение данных пользователя'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(Authorize, db)
    return db_user


@router.put(
    '/me/public',
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}},
    response_model=PublicProfile
)
def update_user_public_profile_data(
    PublicProfileData: PublicProfileModifiable,
    userPublicPicture: UploadFile = File(
        default=False, description='Фото публичного профиля'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    '''Обновление данных публичного профиля пользователя'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(Authorize, db, types=[
                                       settings.UserTypeEnum.musician, settings.UserTypeEnum.radiostaion])
    db_public_profile = UserCruds(db).get_public_profile(user_id=db_user.id)
    db_image = save_image(
        db=db,
        upload_file=userPublicPicture,
        user_id=db_user.id
    )
    db_public_profile_updated = UserCruds(db).update_public_profile(
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


@router.get(
    '/me/public',
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}
    },
    response_model=PublicProfile
)
def get_user_public_profile_info(
        Authorize: AuthJWT = Depends(),
        db: Session = Depends(get_db)):
    '''Получение данных публичного профиля пользователя'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize, db, types=[
            settings.UserTypeEnum.musician,
            settings.UserTypeEnum.radiostaion
        ]
    )
    return UserCruds(db).get_public_profile(user_id=db_user.id)


@router.get('/{user_id}/playlists', response_model=List[PlaylistInfoWithoutTracks])
def get_user_playlists(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
    user_id: int = Query(
        default=None, description='ID пользователя', required=True),
    order_by: order_playlist_by = Query(
        default='created_at', description='Порядок сортировки', required=True),
    order_orientation: Literal['asc', 'desc'] = Query(
        default='asc', description='Направление сортировки', required=True),
):
    '''Получение списка плейлистов'''
    Authorize.jwt_optional()
    db_requested_user = UserCruds(db).get_user_by_id(user_id=user_id)
    if not db_requested_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь не найден'
        )
    current_user_id = Authorize.get_jwt_subject()
    playlists = PlaylistsCrud(db).get_playlists_by_user_id(
        user_id=current_user_id,
        owner_id=user_id,
        order_by=order_by,
        order_orientation=order_orientation
    )
    return playlists
