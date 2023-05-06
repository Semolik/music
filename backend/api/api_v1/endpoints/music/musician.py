from typing import List
from fastapi import Depends, APIRouter, Path, status, HTTPException, Query
from backend.crud.crud_clips import ClipsCruds
from backend.helpers.auth_helper import Authenticate
from backend.schemas.base import LikesInfo
from backend.schemas.music import AlbumInfo, MusicianClip, MusicianContent, Track, MusicianFullInfo, MusicianInfo
from backend.schemas.user import PublicProfile
from backend.crud.crud_user import UserCruds
from backend.crud.crud_musician import MusicianCrud
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.core.config import settings, env_config
router = APIRouter(prefix='/musician', tags=['Музыканты'])


@router.get('/liked', response_model=List[PublicProfile])
def get_liked_musician_profiles(
    Auth: Authenticate = Depends(Authenticate()),
    page: int = Query(1, description='Номер страницы'),
):
    '''Получение списка любимых музыкантов'''
    liked_musician_profiles = MusicianCrud(Auth.db).get_liked_musicians(
        user_id=Auth.current_user_id, page=page)
    for profile in liked_musician_profiles:
        profile.is_liked = True
    return liked_musician_profiles


@router.get('/random', response_model=List[PublicProfile])
def get_random_musician_profiles(
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение списка случайных музыкантов'''
    random_musician_profiles = MusicianCrud(
        Auth.db).get_random_musician_profiles()
    if Auth.current_user_id:
        for profile in random_musician_profiles:
            profile.current_user_id = Auth.current_user_id
    return random_musician_profiles


@router.get('/popular', response_model=List[MusicianInfo])
def get_popular_musician_profiles(
    page: int = Query(1, description='Номер страницы'),
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение списка популярных музыкантов'''
    popular_musician_profiles = MusicianCrud(
        Auth.db).get_popular_musician_profiles(page=page)
    if Auth.current_user_id:
        for profile in popular_musician_profiles:
            profile.current_user_id = Auth.current_user_id
    return popular_musician_profiles


@router.put('/{profile_id}/like', response_model=LikesInfo)
def like_musician(
    profile_id: int = Path(..., description='ID профиля', ge=1),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Лайк музыканта'''

    if not UserCruds(Auth.db).get_public_profile_by_id(id=profile_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    liked = MusicianCrud(Auth.db).toggle_like_musician(
        user_id=Auth.current_user_id,
        musician_id=profile_id)
    likes_count = MusicianCrud(Auth.db).get_musician_likes_count(
        musician_id=profile_id)
    return LikesInfo(liked=liked, likes_count=likes_count)


@router.get('/{profile_id}', response_model=MusicianFullInfo)
def get_public_profile_info(
    profile_id: int = Path(..., description='ID профиля'),
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение информации о публичном профиле музыканта'''

    public_profile = UserCruds(Auth.db).get_public_profile_by_id(id=profile_id)
    if not public_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    public_profile.current_user_id = Auth.current_user_id
    db_tracks = MusicianCrud(Auth.db).get_popular_musician_tracks(
        musician_id=profile_id)
    db_albums = MusicianCrud(Auth.db).get_popular_musician_albums(
        musician_id=profile_id)
    clips = ClipsCruds(Auth.db).get_musician_clips(musician_id=profile_id, page_size=int(
        env_config.get('VITE_CLIP_PAGE_COUNT_MUSICIAN')))

    for track in db_tracks:
        track.current_user_id = Auth.current_user_id
    for album in db_albums:
        album.current_user_id = Auth.current_user_id

    public_profile_obj = MusicianFullInfo(
        **MusicianInfo.from_orm(public_profile).dict(),
        popular=MusicianContent(
            albums=db_albums,
            clips=clips,
            tracks=db_tracks
        )
    )
    return public_profile_obj


@router.get('/{profile_id}/info', response_model=PublicProfile)
def get_public_profile(
    profile_id: int = Path(..., description='ID профиля'),
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение публичного профиля музыканта'''
    public_profile = UserCruds(Auth.db).get_public_profile_by_id(id=profile_id)
    if not public_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    return public_profile


@ router.get('/{profile_id}/clips', response_model=List[MusicianClip])
def get_musician_clips(
    profile_id: int = Path(..., description='ID музыканта'),
    page: int = Query(1, description='Страница'),
    db: Session = Depends(get_db)
):
    '''Получение клипов музыканта'''
    db_public_profile = UserCruds(db).get_public_profile_by_id(id=profile_id)
    if not db_public_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    clips = ClipsCruds(db).get_musician_clips(
        musician_id=db_public_profile.id, page=page)
    return clips


@router.get('/{profile_id}/albums', response_model=List[AlbumInfo])
def get_musician_albums(
    profile_id: int = Path(..., description='ID музыканта'),
    page: int = Query(1, description='Страница'),
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение альбомов музыканта'''
    db_public_profile = UserCruds(
        Auth.db).get_public_profile_by_id(id=profile_id)
    if not db_public_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    albums = MusicianCrud(Auth.db).get_popular_musician_albums(
        musician_id=db_public_profile.id, page=page, page_size=settings.ALBUM_PAGE_COUNT_ALL)
    return albums


@router.get('/{profile_id}/popular', response_model=List[Track])
def get_musician_popular_tracks(
    profile_id: int = Query(..., description='ID музыканта'),
    page: int = Query(1, description='Страница'),
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение популярных треков музыканта'''
    db_public_profile = UserCruds(
        Auth.db).get_public_profile_by_id(id=profile_id)
    if not db_public_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    tracks = MusicianCrud(Auth.db).get_popular_musician_tracks(
        musician_id=db_public_profile.id, page=page
    )
    if Auth.current_user_id:
        for track in tracks:
            track.current_user_id = Auth.current_user_id
    return tracks


@router.get('/{profile_id}/popular/search', response_model=List[Track])
def search_musician_popular_tracks(
    profile_id: int = Query(..., description='ID музыканта'),
    search: str = Query(..., description='Поисковый запрос'),
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Поиск популярных треков музыканта'''
    db_public_profile = UserCruds(
        Auth.db).get_public_profile_by_id(id=profile_id)
    if not db_public_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Профиль музыканта не найден")
    tracks = MusicianCrud(Auth.db).search_popular_musician_tracks(
        musician_id=db_public_profile.id, search=search
    )
    if Auth.current_user_id:
        for track in tracks:
            track.current_user_id = Auth.current_user_id
    return tracks
