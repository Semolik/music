from typing import List
from fastapi import Depends, APIRouter, Path, File, status, HTTPException, Query
from backend.helpers.auth_helper import Authenticate
from backend.schemas.history import HistoryItem
from backend.schemas.music import Track
from backend.crud.crud_history import HistoryCrud

router = APIRouter(prefix="/history", tags=['История'])


@router.get('', response_model=List[HistoryItem])
def get_history(
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение истории'''
    return HistoryCrud(Auth.db).get_history(user_id=Auth.current_user_id)


@router.get('/tracks', response_model=List[Track])
def get_history_tracks(
    page: int = Query(1, ge=1),
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение треков из истории'''
    return HistoryCrud(Auth.db).get_tracks_history(user_id=Auth.current_user_id, page=page)
