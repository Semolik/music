from datetime import datetime
from typing import List
from backend.db.base import CRUDBase
from backend.helpers.roles import post_processing_change_role_messages, set_status
from backend.helpers.images import set_picture
from backend.core.config import settings
from backend.helpers.files import set_files_data
from backend.schemas.user import ChangeRoleRequestInfo
from backend.models.roles import AnswerChangeRoleRequest, ChangeRoleRequest

from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status


class ChangeRolesCruds(CRUDBase):
    def send_change_role_message(self, user_id, message, files, account_status):
        db_change_role_request = ChangeRoleRequest(
            files=files,
            message=message,
            user_id=user_id,
            account_status=account_status
        )
        return self.create(db_change_role_request)

    def get_user_change_role_messages(self, user_id):
        records: List[ChangeRoleRequest] =\
            self.db.query(ChangeRoleRequest)\
            .order_by(ChangeRoleRequest.id.desc())\
            .filter(ChangeRoleRequest.user_id == user_id)\
            .all()
        return post_processing_change_role_messages(records)

    def get_all_change_role_messages(self, page: int = 1, filter: str = 'all', page_size: int = 10) -> List[ChangeRoleRequest]:
        end = page * page_size
        query = self.db.query(ChangeRoleRequest).order_by(
            ChangeRoleRequest.id.desc())
        if filter != 'all':
            query = query.where(ChangeRoleRequest.status == filter)
        return post_processing_change_role_messages(query.slice(end-page_size, end), add_user=True)

    def is_has_change_role_messages(self, user_id):
        return bool(self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.user_id == user_id).first())

    def is_user_have_active_change_role_messages(self, user_id: int, count: int) -> bool:
        result = self.db.query(ChangeRoleRequest)\
            .filter(ChangeRoleRequest.user_id == user_id, ChangeRoleRequest.status == 'in-progress')\
            .limit(count).all()
        return len(result) == count

    def get_change_role_message(self, request_id):
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.id == request_id).first()

    def send_change_role_message_answer(self, request: ChangeRoleRequest, message: str, request_status: settings.ALLOWED_STATUSES, account_status: str = None):
        if request.answer:
            self.db.delete(request.answer)
            self.db.commit()
        db_answer = AnswerChangeRoleRequest(
            message=message,
            request_id=request.id
        )
        db_answer = self.create(db_answer)
        set_status_result = True
        if account_status:
            set_status_result = set_status(
                self.db, request.user, account_status)
        elif request_status == 'successfully':
            set_status_result = set_status(
                self.db, request.user, request.account_status)
        if not set_status_result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Попытка установить неподдерживаемый статус аккаунта")
        request.answer = db_answer
        request.status = request_status
        self.db.commit()
        answer_obj = jsonable_encoder(db_answer)
        answer_obj['time_created'] = db_answer.time_created.strftime(
            settings.DATETIME_FORMAT)
        return answer_obj

    def get_not_answered_change_role_request_count(self):
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.status == 'in-progress').count()
