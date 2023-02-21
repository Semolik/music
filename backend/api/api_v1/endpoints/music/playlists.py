from uuid import UUID
from fastapi import Depends, APIRouter, status, HTTPException, Query
from fastapi_jwt_auth import AuthJWT
from backend.crud.crud_playlists import PlaylistsCrud
from backend.crud.crud_tracks import TracksCrud
from backend.helpers.auth_helper import validate_authorized_user
from backend.helpers.music import is_playlist_showed, validate_tracks, validate_track
from backend.schemas.playlists import PlaylistInfo, PlaylistCreate, TracksIds
from backend.db.db import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix='/playlists', tags=['Плейлисты'])


@router.get('/{playlist_id}', response_model=PlaylistInfo)
def get_playlist_info(
    playlist_id: UUID = Query(..., description='ID плейлиста'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    '''Получение информации о плейлисте'''
    Authorize.jwt_optional()
    current_user_id = Authorize.get_jwt_subject()
    playlist_crud = PlaylistsCrud(db)
    playlist = playlist_crud.get_playlist_info(playlist_id=playlist_id)
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Плейлист не найден")
    if not is_playlist_showed(playlist=playlist, user_id=current_user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Плейлист не найден")
    playlist_obj = PlaylistInfo.from_orm(playlist)
    playlist_obj.tracks = playlist_crud.get_tracks_by_playlist_id(
        playlist_id=playlist_id, user_id=current_user_id)
    return playlist


@router.post('', response_model=PlaylistInfo)
def create_playlist(
    playlist: PlaylistCreate,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    '''Создание плейлиста'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db)
    db_tracks = validate_tracks(
        tracks_ids=playlist.tracks_ids, db=db, user_id=db_user.id)
    playlist_crud = PlaylistsCrud(db)
    created_playlist = playlist_crud.create_playlist(
        name=playlist.name,
        description=playlist.description,
        user_id=db_user.id,
        private=playlist.private,
        tracks_ids=[track.id for track in db_tracks]
    )
    playlist_obj = PlaylistInfo.from_orm(created_playlist)
    playlist_obj.tracks = db_tracks
    return playlist_obj


# @router.put('/{playlist_id}', response_model=PlaylistInfo)
# def update_playlist(
#     playlist: PlaylistCreate,
#     playlist_id: int = Query(..., description='ID плейлиста'),
#     Authorize: AuthJWT = Depends(),
#     db: Session = Depends(get_db),
# ):
    # '''Обновление плейлиста'''
    # Authorize.jwt_required()
    # db_user = validate_authorized_user(
    #     Authorize=Authorize, db=db)
    # db_tracks = validate_tracks(
    #     tracks_ids=playlist.tracks_ids, db=db, user_id=db_user.id)
    # db_playlist = PlaylistsCrud(db).get_playlist_info(playlist_id=playlist_id)
    # if not db_playlist or db_playlist.user_id != db_user.id:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="Плейлист не найден")
    # return PlaylistsCrud(db).update_playlist(
    #     playlist_id=playlist_id,
    #     name=playlist.name,
    #     description=playlist.description,
    #     private=playlist.private,
    #     tracks_ids=[track.id for track in db_tracks]
    # )


@router.post('/{playlist_id}/track', response_model=PlaylistInfo)
def add_track_to_playlist(
    track_id: UUID = Query(..., description='ID трека'),
    playlist_id: UUID = Query(..., description='ID плейлиста'),
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    '''Добавление трека в плейлист'''
    Authorize.jwt_required()
    db_user = validate_authorized_user(
        Authorize=Authorize, db=db)
    db_track = validate_track(track_id=track_id, db=db, user_id=db_user.id)
    playlist_crud = PlaylistsCrud(db)
    db_playlist = playlist_crud.get_playlist_info(playlist_id=playlist_id)
    if not db_playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Плейлист не найден")
    if db_playlist.user_id != db_user.id:
        if db_playlist.private:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Плейлист не найден")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Нет доступа")
    if db_track in playlist_crud.get_tracks_by_playlist_id(playlist_id=playlist_id, user_id=db_user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Трек уже есть в плейлисте")
    return playlist_crud.add_track_to_playlist(
        playlist_id=playlist_id,
        track_id=track_id,
        user_id=db_user.id
    )
    # db_tracks = validate_tracks(
    #     tracks_ids=tracks_data.tracks_ids, db=db, user_id=db_user.id)
    # playlist_crud = PlaylistsCrud(db)
    # db_playlist = playlist_crud.get_playlist_info(playlist_id=playlist_id)
    # if not db_playlist or db_playlist.user_id != db_user.id:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail="Плейлист не найден")
    # for track in db_tracks:
    #     if track in playlist_crud.get_tracks_by_playlist_id(playlist_id=playlist_id, user_id=db_user.id):
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                             detail="Трек уже есть в плейлисте")
    # return playlist_crud.add_tracks_to_playlist(
    #     db_playlist=db_playlist,
    #     db_tracks=db_tracks,
    #     user_id=db_user.id
    # )
