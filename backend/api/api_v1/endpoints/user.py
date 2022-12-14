from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.helpers.images import save_image, set_picture
from backend.helpers.users import get_public_profile_as_dict, get_public_profile_data
from backend.schemas.user import PublicProfile, PublicProfileModifiable, UserInfo, UserModifiableForm
from backend.schemas.error import HTTP_401_UNAUTHORIZED
from backend.crud.crud_user import UserCruds
from backend.db.db import get_db
from sqlalchemy.orm import Session
router = APIRouter(tags=['Профили пользователей'])


@router.put('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def update_user_data(
        UserData: UserModifiableForm = Depends(UserModifiableForm),
        userPicture: UploadFile = File(default=False),
        Authorize: AuthJWT = Depends(),
        db: Session = Depends(get_db)
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = UserCruds(db).get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
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
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user = UserCruds(db).get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    user_data = user.as_dict()
    user_data = set_picture(user_data, user.picture)
    return user_data


@router.put(
    '/me/public',
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}},
    response_model=PublicProfile
)
def update_user_public_profile_data(
    PublicProfileData: PublicProfileModifiable = Depends(
        PublicProfileModifiable
    ),
    userPublicPicture: UploadFile = File(default=False),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = UserCruds(db).get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден")
    if not db_user.type == 'musician' and not db_user.type == 'radio_station':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Аккаунт должен иметь статус музыкант или радиостанция")
    db_public_profile = UserCruds(
        db).get_public_profile(user_id=current_user_id)
    db_image = save_image(db=db, upload_file=userPublicPicture,
                          user_id=db_user.id)
    db_public_profile_updated = UserCruds(db).update_public_profile(
        public_proile=db_public_profile, new_public_proile_data=PublicProfileData, userPublicPicture=db_image)
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
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = UserCruds(db).get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден")
    if not db_user.type == 'musician' and not db_user.type == 'radio_station':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Аккаунт должен иметь статус музыкант или радиостанция")
    return get_public_profile_as_dict(db=db, user_id=current_user_id)
