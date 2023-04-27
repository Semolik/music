from typing import List
from fastapi import Depends, APIRouter, Path, File, status, HTTPException
from backend.helpers.auth_helper import Authenticate
from backend.schemas.history import HistoryItem
from backend.crud.crud_history import HistoryCrud

router = APIRouter(prefix="/history", tags=['История'])


@router.get('', response_model=List[HistoryItem])
def get_history(
    Auth: Authenticate = Depends(Authenticate()),
):
    '''Получение истории'''
    return HistoryCrud(Auth.db).get_history(user_id=Auth.current_user_id)
