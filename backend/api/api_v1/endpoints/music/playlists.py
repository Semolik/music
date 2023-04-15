from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter, Path, status, HTTPException, Query
from backend.crud.crud_playlists import PlaylistsCrud
from backend.helpers.auth_helper import Authenticate
from backend.helpers.music import is_playlist_showed, set_tracks_likes, validate_playlist_owner, validate_public_playlist, validate_tracks, validate_track
from backend.schemas.playlists import PlaylistBase, PlaylistInfo, PlaylistCreate, PlaylistInfoWithoutTracks, PlaylistTrack, order_playlist_by
from backend.core.config import settings
router = APIRouter(prefix='/playlists', tags=['Плейлисты'])


@router.get('', response_model=List[PlaylistInfoWithoutTracks])
def get_my_playlists(
    order_by: order_playlist_by = Query(
        default=order_playlist_by.created_at, description='Порядок сортировки'),
    order_orientation: settings.Order = Query(
        default=settings.Order.asc, description='Направление сортировки'),
    owned_only: bool = Query(
        default=False, description='Показывать только мои плейлисты'),
    private: bool = Query(
        default=False, description='Показывать только приватные плейлисты'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение списка плейлистов'''
    if not order_orientation:
        order_orientation = settings.Order.asc
    if not order_by:
        order_by = order_playlist_by.created_at
    playlists = PlaylistsCrud(Auth.db).get_playlists_by_user_id(
        user_id=Auth.current_user_id,
        owner_id=Auth.current_user_id,
        order_by=order_by,
        order_orientation=order_orientation,
        owned_only=owned_only,
        private=private
    )
    playlists_objs = []
    for playlist in playlists:
        playlist_obj = PlaylistInfoWithoutTracks.from_orm(playlist)
        playlist_obj.liked = PlaylistsCrud(Auth.db).is_playlist_liked(
            playlist_id=playlist.id,
            user_id=Auth.current_user_id
        )
        playlists_objs.append(playlist_obj)
    return playlists


@router.get('/{playlist_id}', response_model=PlaylistInfo)
def get_playlist_info(
    playlist_id: UUID = Path(..., description='ID плейлиста'),
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение информации о плейлисте'''

    playlist_crud = PlaylistsCrud(Auth.db)
    playlist = playlist_crud.get_playlist_info(playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Плейлист не найден")
    if not is_playlist_showed(playlist=playlist, user_id=Auth.current_user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Плейлист не найден")
    playlist_obj = PlaylistInfo.from_orm(playlist)
    playlist_obj.tracks = set_tracks_likes(tracks=playlist_crud.get_tracks_by_playlist_id(
        playlist_id=playlist_id,
        user_id=Auth.current_user_id
    ), user_id=Auth.current_user_id, db=Auth.db)
    return playlist_obj


@router.post('', response_model=PlaylistInfo)
def create_playlist(
    playlist: PlaylistCreate,
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Создание плейлиста'''

    db_tracks = validate_tracks(
        tracks_ids=playlist.tracks_ids, db=Auth.db, user_id=Auth.current_user_id)
    playlist_crud = PlaylistsCrud(Auth.db)
    created_playlist = playlist_crud.create_playlist(
        name=playlist.name,
        description=playlist.description,
        user_id=Auth.current_user_id,
        private=playlist.private,
        tracks_ids=[track.id for track in db_tracks]
    )
    playlist_obj = PlaylistInfo.from_orm(created_playlist)
    playlist_obj.tracks = set_tracks_likes(
        tracks=db_tracks, user_id=Auth.current_user_id, db=Auth.db)
    return playlist_obj


@router.put('/{playlist_id}', response_model=PlaylistInfo)
def update_playlist(
    playlist: PlaylistBase,
    playlist_id: UUID = Path(..., description='ID плейлиста'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Обновление плейлиста'''

    db_playlist = validate_playlist_owner(
        playlist_id=playlist_id, db=Auth.db, user_id=Auth.current_user_id)
    playlist_crud = PlaylistsCrud(Auth.db)
    updated_playlist = playlist_crud.update_playlist(
        playlist=db_playlist,
        name=playlist.name,
        description=playlist.description,
        private=playlist.private
    )
    playlist_obj = PlaylistInfo.from_orm(updated_playlist)
    playlist_obj.tracks = set_tracks_likes(
        tracks=playlist_crud.get_tracks_by_playlist_id(
            playlist_id=playlist_id, user_id=Auth.current_user_id),
        user_id=Auth.current_user_id,
        db=Auth.db
    )
    return playlist_obj


@router.post('/{playlist_id}/track/{track_id}', response_model=PlaylistTrack)
def add_track_to_playlist(
    track_id: UUID = Path(..., description='ID трека'),
    playlist_id: UUID = Path(..., description='ID плейлиста'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Добавление трека в плейлист'''

    validate_track(track_id=track_id, db=Auth.db, user_id=Auth.current_user_id)
    validate_playlist_owner(playlist_id=playlist_id,
                            db=Auth.db, user_id=Auth.current_user_id)
    playlist_crud = PlaylistsCrud(Auth.db)
    if playlist_crud.get_playlist_track(playlist_id=playlist_id, track_id=track_id, user_id=Auth.current_user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Трек уже есть в плейлисте")
    return playlist_crud.add_track_to_playlist(
        playlist_id=playlist_id,
        track_id=track_id
    )


@router.delete('/{playlist_id}/track/{track_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_track_from_playlist(
    track_id: UUID = Path(..., description='ID трека'),
    playlist_id: UUID = Path(..., description='ID плейлиста'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Удаление трека из плейлиста'''

    validate_track(track_id=track_id, db=Auth.db, user_id=Auth.current_user_id)
    validate_playlist_owner(playlist_id=playlist_id,
                            db=Auth.db, user_id=Auth.current_user_id)
    playlist_crud = PlaylistsCrud(Auth.db)
    playlist_track = playlist_crud.get_playlist_track(
        playlist_id=playlist_id, track_id=track_id, user_id=Auth.current_user_id)
    if not playlist_track:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Трека нет в плейлисте")
    playlist_crud.delete(playlist_track)


@router.delete('/{playlist_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_playlist(
    playlist_id: UUID = Path(..., description='ID плейлиста'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Удаление плейлиста'''
    playlist = validate_playlist_owner(
        playlist_id=playlist_id, db=Auth.db, user_id=Auth.current_user_id)
    PlaylistsCrud(Auth.db).delete(playlist)


@router.put('/{playlist_id}/like', response_model=bool)
def like_playlist(
    playlist_id: UUID = Path(..., description='ID плейлиста'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Лайк плейлиста'''
    playlist = validate_public_playlist(
        playlist_id=playlist_id, db=Auth.db, user_id=Auth.current_user_id
    )

    return PlaylistsCrud(Auth.db).toggle_like_playlist(playlist_id=playlist.id, user_id=Auth.current_user_id)
