from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.helpers.auth_helper import validate_authorized_user
from backend.helpers.images import save_image, set_picture
from backend.helpers.users import get_public_profile_as_dict, get_public_profile_data
from backend.schemas.user import PublicProfile, PublicProfileModifiable, UserInfo, UserModifiable
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.crud.crud_user import UserCruds
from backend.db.db import get_db
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
    db_user_updated = UserCruds(db).update(
        user=db_user, new_user_data=UserData, userPic=db_image)
    user_data = db_user_updated.as_dict()
    user_data = set_picture(user_data, db_user_updated.picture)
    return user_data


@router.get('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def get_user_info(Authorize: AuthJWT = Depends(),
                  db: Session = Depends(get_db)):
    '''Получение данных пользователя'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(Authorize, db)
    user_obj = db_user.as_dict()
    user_data = set_picture(user_obj, db_user.picture)
    return user_data


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
    db_user = validate_authorized_user(Authorize, db)
    if not db_user.type == 'musician' and not db_user.type == 'radio_station':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Аккаунт должен иметь статус музыкант или радиостанция")
    db_public_profile = UserCruds(db).get_public_profile(user_id=db_user.id)
    db_image = save_image(
        db=db,
        upload_file=userPublicPicture,
        user_id=db_user.id
    )
    db_public_profile_updated = UserCruds(db).update_public_profile(
        public_proile=db_public_profile,
        new_public_proile_data=PublicProfileData,
        userPublicPicture=db_image
    )
    return get_public_profile_data(db_public_profile=db_public_profile_updated, full_links=False)


@router.get('/me/public',
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "model": HTTP_401_UNAUTHORIZED
                }
            },
            response_model=PublicProfile
            )
def get_user_public_profile_info(Authorize: AuthJWT = Depends(),
                                 db: Session = Depends(get_db)):
    '''Получение данных публичного профиля пользователя'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(Authorize, db)
    if not db_user.type == 'musician' and not db_user.type == 'radio_station':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Аккаунт должен иметь статус музыкант или радиостанция")
    return get_public_profile_as_dict(db=db, user_id=db_user.id)
