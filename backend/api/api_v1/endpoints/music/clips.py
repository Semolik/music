from typing import List
from fastapi import Depends, APIRouter, UploadFile, File, status, HTTPException
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_clips import clips_cruds
from backend.crud.crud_user import user_cruds
from backend.helpers.images import save_image
from backend.helpers.clips import set_clip_data
from backend.helpers.validate_role import validate_musician
from backend.schemas.music import CreateMusicianClipForm, MusicianClip, UpdateMusicianClipForm
from backend.helpers.files import save_image_in_db_by_url
router = APIRouter(prefix="/clips", tags=['Клипы'])


@router.post('/clip', response_model=MusicianClip)
def create_clip(clipData: CreateMusicianClipForm = Depends(CreateMusicianClipForm), clipPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_musician(user_id=current_user_id)
    db_public_profile = user_cruds.get_public_profile(user_id=current_user_id)
    if clipData.image_from_youtube:
        image_model = save_image_in_db_by_url(
            f'http://img.youtube.com/vi/{clipData.video_id}/hqdefault.jpg', user_id=current_user_id)
    else:
        image_model = save_image(upload_file=clipPicture,
                                 user_id=current_user_id, resize_image_options=(1000, 1000))
    if not image_model:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Необходимо или передать картинку или указать image_from_youtube = true")
    clip = clips_cruds.create_clip(
        musician_id=db_public_profile.id, video_id=clipData.video_id, name=clipData.name, image_model=image_model)
    return set_clip_data(clip=clip)


@router.delete('/clip')
def delete_clip(clip_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_musician(user_id=current_user_id)
    db_public_profile = user_cruds.get_public_profile(user_id=current_user_id)
    db_clip = clips_cruds.get_clip_by_id(clip_id=clip_id)
    if not db_clip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Клип не найден")
    if db_clip.musician_id != db_public_profile.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Вы не можете изменять этот клип")
    clips_cruds.delete(model=db_clip)
    return {'detail': "Клип удален"}


@router.put('/clip', response_model=MusicianClip)
def update_clip(clipData: UpdateMusicianClipForm = Depends(UpdateMusicianClipForm), clipPicture: UploadFile = File(default=False), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_musician(user_id=current_user_id)
    db_public_profile = user_cruds.get_public_profile(user_id=current_user_id)
    db_clip = clips_cruds.get_clip_by_id(clip_id=clipData.id)
    if not db_clip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Клип не найден")
    if db_clip.musician_id != db_public_profile.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Вы не можете изменять этот клип")
    if clipData.image_from_youtube:
        image_model = save_image_in_db_by_url(
            f'http://img.youtube.com/vi/{clipData.video_id}/hqdefault.jpg', user_id=current_user_id)
    else:
        image_model = save_image(upload_file=clipPicture,
                                 user_id=current_user_id, resize_image_options=(1000, 1000))
    clip = clips_cruds.update_clip(
        db_clip=db_clip, video_id=clipData.video_id, name=clipData.name, image=image_model)
    return set_clip_data(clip=clip)


@router.get('/clip', response_model=MusicianClip)
def create_clip(id: int):
    clip = clips_cruds.get_clip_by_id(clip_id=id)
    if not clip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Клип не найден")
    return set_clip_data(clip=clip)


@router.get('/all', response_model=List[MusicianClip])
def get_my_clips(musician_id: int, page: int):
    db_public_profile = user_cruds.get_public_profile_by_id(id=musician_id)
    if not db_public_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    clips = clips_cruds.get_musician_clips(
        musician_id=db_public_profile.id, page=page)
    return [set_clip_data(clip=clip) for clip in clips]


@router.get('/my', response_model=List[MusicianClip])
def get_my_clips(page: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    validate_musician(user_id=current_user_id)
    db_public_profile = user_cruds.get_public_profile(user_id=current_user_id)
    clips = clips_cruds.get_musician_clips(
        musician_id=db_public_profile.id, page=page)
    return [set_clip_data(clip=clip) for clip in clips]
