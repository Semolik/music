from backend.models.user import User
from backend.core.config import settings
from backend.db.session import SessionLocal


def set_status(db: SessionLocal, user: User, status: settings.USER_ACCOUNT_STATUSES):
    if status not in settings.USER_ACCOUNT_STATUSES_LIST:
        return
    user.type = status
    db.commit()
    return user
