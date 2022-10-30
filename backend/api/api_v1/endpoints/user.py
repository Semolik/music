from fastapi import Depends, APIRouter, status, UploadFile, File, HTTPException
from fastapi_jwt_auth import AuthJWT
from helpers.files import save_file
from helpers.images import set_picture
from schemas.user import PublicProfile, PublicProfileLinks, PublicProfileModifiable, UserInfo, UserModifiableForm
from schemas.error import HTTP_401_UNAUTHORIZED
from crud.crud_user import user_cruds
router = APIRouter(tags=['Профили пользователей'])


@router.put('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def update_user_data(UserData: UserModifiableForm = Depends(UserModifiableForm), userPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    db_image = save_file(upload_file=userPicture,
                         user_id=db_user.id, force_image=True)
    db_user_updated = user_cruds.update(
        user=db_user, new_user_data=UserData, userPic=db_image)
    user_data = db_user_updated.as_dict()
    user_data = set_picture(user_data, db_user_updated.picture)
    return user_data


@router.get('/me', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=UserInfo)
def get_user_info(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user = user_cruds.get_user_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="неправильное имя пользователя или пароль")
    user_data = user.as_dict()
    user_data = set_picture(user_data, user.picture)
    return user_data


@router.put('/me/public', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}})
def update_user_public_profile_data(PublicProfileData: PublicProfileModifiable = Depends(PublicProfileModifiable), links: PublicProfileLinks = Depends(PublicProfileLinks),  userPublicPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден")
    if not db_user.is_musician and not db_user.is_radio_station:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Аккаунт должен иметь статус музыкант или радиостанция")
    db_public_profile = user_cruds.get_public_profile(user_id=current_user_id)
    db_image = save_file(upload_file=userPublicPicture,
                         user_id=db_user.id, force_image=True)
    db_public_profile_updated = user_cruds.update_public_profile(
        public_proile=db_public_profile, new_public_proile_data=PublicProfileData, new_public_proile_links=links, userPublicPicture=db_image)
    public_profile_data = db_public_profile_updated.as_dict()
    public_profile_data['links'] = db_public_profile_updated.links
    public_profile_data = set_picture(
        public_profile_data, db_public_profile_updated.picture)
    return public_profile_data


@router.get('/me/public', responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTP_401_UNAUTHORIZED}}, response_model=PublicProfile)
def get_user_public_profile_info(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    db_user = user_cruds.get_user_by_id(current_user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Пользователь не найден")
    if not db_user.is_musician and not db_user.is_radio_station:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Аккаунт должен иметь статус музыкант или радиостанция")
    db_public_profile = user_cruds.get_public_profile(user_id=current_user_id)
    public_profile_data = db_public_profile.as_dict()
    public_profile_data['links'] = db_public_profile.links.as_dict()
    return public_profile_data
