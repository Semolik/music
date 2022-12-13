from datetime import datetime
from typing import List
from backend.helpers.files import set_files_data
from backend.helpers.images import set_picture
from backend.models.roles import ChangeRoleRequest
from backend.models.user import User
from backend.core.config import settings
from backend.db.session import SessionLocal
from fastapi.encoders import jsonable_encoder

from backend.schemas.user import ChangeRoleRequestInfo


def set_status(db: SessionLocal, user: User, status: settings.USER_ACCOUNT_STATUSES):
    if status not in settings.USER_ACCOUNT_STATUSES_LIST:
        return
    user.type = status
    db.commit()
    return user


def post_processing_change_role_messages(records: List[ChangeRoleRequest], add_user=False) -> ChangeRoleRequestInfo:
    result = list()
    for record in records:
        time_created: datetime = record.time_created
        time_created_str = time_created.strftime(settings.DATETIME_FORMAT)
        record_obj = jsonable_encoder(record)
        record_obj['answer'] = jsonable_encoder(record.answer)
        if add_user:
            user = record.user
            user_obj = jsonable_encoder(user)
            user_obj_with_pic = set_picture(user_obj, user.picture)
            record_obj['user'] = user_obj_with_pic
        record_obj['files'] = set_files_data(files=record.files)
        record_obj['time_created'] = time_created_str
        result.append(record_obj)
    return result
