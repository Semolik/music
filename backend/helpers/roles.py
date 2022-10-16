from models.user import User
from core.config import settings
from db.session import SessionLocal


def set_status(db: SessionLocal, user: User, status: settings.USER_ACCOUNT_STATUSES):
    if status not in settings.USER_ACCOUNT_STATUSES_LIST:
        return
    user.is_musician = False
    user.is_radio_station = False
    if status == 'is_radio_station':
        user.is_radio_station = True
    if status == 'is_musician':
        user.is_musician = True
    db.commit()
    return user