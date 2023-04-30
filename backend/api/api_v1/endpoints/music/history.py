from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter, Path, status, HTTPException, Query
from backend.helpers.auth_helper import Authenticate
from backend.helpers.music import is_playlist_showed
from backend.schemas.history import HistoryAlbum, HistoryItem, HistoryMusician, HistoryPlaylist, HistoryTrack
from backend.crud.crud_history import HistoryCrud
from backend.crud.crud_playlists import PlaylistsCrud
from backend.crud.crud_albums import AlbumsCruds
from backend.crud.crud_user import UserCruds
router = APIRouter(prefix="/history", tags=['История'])


@router.get('', response_model=List[HistoryItem])
def get_history(
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение последних прослушанных плейлистов, альбомов и музыкантов'''
    return HistoryCrud(Auth.db).get_history(user_id=Auth.current_user_id)


@router.get('/tracks', response_model=List[HistoryTrack])
def get_history_tracks(
    page: int = Query(1, ge=1),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение треков из истории'''
    return HistoryCrud(Auth.db).get_tracks_history(user_id=Auth.current_user_id, page=page)


@router.post('/playlists/{playlist_id}', status_code=status.HTTP_201_CREATED, response_model=HistoryPlaylist)
def add_playlist_to_history(
    playlist_id: UUID = Path(..., description='ID плейлиста'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Добавление плейлиста в историю'''
    playlist = PlaylistsCrud(Auth.db).get_playlist_info(
        playlist_id=playlist_id)
    if not playlist or not is_playlist_showed(playlist=playlist, user_id=Auth.current_user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Плейлист не найден")
    return HistoryCrud(Auth.db).add_playlist_to_history(
        playlist_id=playlist_id, user_id=Auth.current_user_id)


@router.post('/albums/{album_id}', status_code=status.HTTP_201_CREATED, response_model=HistoryAlbum)
def add_album_to_history(
    album_id: UUID = Path(..., description='ID альбома'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Добавление альбома в историю'''
    album = AlbumsCruds(Auth.db).get_album(album_id=album_id)
    if not album or not album.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Альбом не найден")
    return HistoryCrud(Auth.db).add_album_to_history(
        album_id=album_id, user_id=Auth.current_user_id)


@router.post('/musicians/{musician_id}', status_code=status.HTTP_201_CREATED, response_model=HistoryMusician)
def add_musician_to_history(
    musician_id: UUID = Path(..., description='ID музыканта'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Добавление музыканта в историю'''
    musician = UserCruds(Auth.db).get_public_profile_by_id(id=musician_id)
    if not musician:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Музыкант не найден")
    return HistoryCrud(Auth.db).add_musician_to_history(
        musician_id=musician_id, user_id=Auth.current_user_id)


@router.delete('/tracks/{history_item_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_track_from_history(
    history_item_id: UUID = Path(..., description='ID элемента истории'),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Удаление трека из истории'''
    history_item = HistoryCrud(Auth.db).get_track_history_item(
        history_item_id=history_item_id)
    if not history_item or history_item.user_id != Auth.current_user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Элемент истории не найден')
    HistoryCrud(Auth.db).delete(history_item)
