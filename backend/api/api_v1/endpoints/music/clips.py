from typing import List
from fastapi import Depends, APIRouter, UploadFile, File, status, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.core.config import settings
from backend.crud.crud_clips import ClipsCruds
from backend.crud.crud_user import UserCruds
from backend.helpers.auth_helper import Authenticate
from backend.helpers.images import save_image
from backend.helpers.clips import video_is_exists
from backend.schemas.music import CreateMusicianClipForm, MusicianClip
from backend.helpers.files import save_image_in_db_by_url
from backend.db.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clips", tags=['Клипы'])


@router.post('', response_model=MusicianClip, status_code=status.HTTP_201_CREATED)
def create_clip(
    clipData: CreateMusicianClipForm = Depends(CreateMusicianClipForm),
    clipPicture: UploadFile = File(
        default=False, description='Картинка клипа'),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Создание клипа'''

    db_public_profile = UserCruds(
        Auth.db).get_public_profile(user_id=Auth.current_user_id)
    if not video_is_exists(clipData.video_id):
        raise HTTPException(status_code=404, detail="ролик не найден")
    if clipData.image_from_youtube:
        image_model = save_image_in_db_by_url(
            db=Auth.db,
            url=f'http://img.youtube.com/vi/{clipData.video_id}/hqdefault.jpg',
            user_id=Auth.current_user_id,
        )
    else:
        image_model = save_image(
            db=Auth.db,
            upload_file=clipPicture,
            user_id=Auth.current_user_id,
            resize_image_options=(1000, 1000)
        )
    if not image_model:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Необходимо или передать картинку или указать image_from_youtube = true")
    clip = ClipsCruds(Auth.db).create_clip(
        musician_id=db_public_profile.id, video_id=clipData.video_id, name=clipData.name, image_model=image_model)
    return clip


@router.delete('/{clip_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_clip(
    clip_id: int = Query(..., description='ID клипа'),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Удаление клипа'''

    db_public_profile = UserCruds(
        Auth.db).get_public_profile(user_id=Auth.current_user_id)
    db_clip = ClipsCruds(Auth.db).get_clip_by_id(clip_id=clip_id)
    if not db_clip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Клип не найден")
    if db_clip.musician_id != db_public_profile.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Вы не можете изменять этот клип")
    ClipsCruds(Auth.db).delete(model=db_clip)


@router.put('/{clip_id}', response_model=MusicianClip)
def update_clip(
    clip_id: int = Query(..., description='ID клипа'),
    clipData: CreateMusicianClipForm = Depends(CreateMusicianClipForm),
    clipPicture: UploadFile = File(
        default=False, description='Картинка клипа'),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Изменение клипа'''

    db_public_profile = UserCruds(
        Auth.db).get_public_profile(user_id=Auth.current_user_id)
    db_clip = ClipsCruds(Auth.db).get_clip_by_id(clip_id=clip_id)
    if not db_clip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Клип не найден")
    if db_clip.musician_id != db_public_profile.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Вы не можете изменять этот клип")
    if not video_is_exists(clipData.video_id):
        raise HTTPException(status_code=404, detail="ролик не найден")
    if clipData.image_from_youtube:
        image_model = save_image_in_db_by_url(
            db=Auth.db,
            url=f'http://img.youtube.com/vi/{clipData.video_id}/hqdefault.jpg',
            user_id=Auth.current_user_id,
        )
    else:
        image_model = save_image(
            db=Auth.db,
            upload_file=clipPicture,
            user_id=Auth.current_user_id,
            resize_image_options=(1000, 1000)
        )
    clip = ClipsCruds(Auth.db).update_clip(
        db_clip=db_clip, video_id=clipData.video_id, name=clipData.name, image=image_model)
    return clip


@router.get('/my', response_model=List[MusicianClip])
def get_my_clips(
    page: int = Query(1, description='Страница'),
    Auth: Authenticate = Depends(Authenticate(is_musician=True)),
):
    '''Получение моих клипов'''

    db_public_profile = UserCruds(
        Auth.db).get_public_profile(user_id=Auth.current_user_id)
    clips = ClipsCruds(Auth.db).get_musician_clips(
        musician_id=db_public_profile.id, page=page)
    return clips


@router.get('/{clip_id}', response_model=MusicianClip)
def get_clip_by_id(
    clip_id: int = Query(..., description='ID клипа'),
    db: Session = Depends(get_db)
):
    '''Получение клипа'''
    clip = ClipsCruds(db).get_clip_by_id(clip_id=clip_id)
    if not clip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Клип не найден")
    return clip
