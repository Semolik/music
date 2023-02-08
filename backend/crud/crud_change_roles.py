from typing import List
from backend.db.base import CRUDBase
from backend.core.config import settings
from backend.models.user import User
from backend.models.roles import AnswerChangeRoleRequest, ChangeRoleRequest, ChangeRoleRequestStatus


class ChangeRolesCruds(CRUDBase):
    def send_change_role_message(self, user_id, message, files, account_status: settings.UserTypeEnum) -> ChangeRoleRequest:
        db_change_role_request = ChangeRoleRequest(
            files=files,
            message=message,
            user_id=user_id,
            requested_account_status=account_status
        )
        return self.create(db_change_role_request)

    def get_user_change_role_messages(self, user_id):
        records: List[ChangeRoleRequest] =\
            self.db.query(ChangeRoleRequest)\
            .order_by(ChangeRoleRequest.id.desc())\
            .filter(ChangeRoleRequest.user_id == user_id)\
            .all()
        return records

    def get_all_change_role_messages(self, page: int = 1, filter: ChangeRoleRequestStatus = None, page_size: int = 10) -> List[ChangeRoleRequest]:
        end = page * page_size
        query = self.db.query(ChangeRoleRequest).order_by(
            ChangeRoleRequest.id.desc())
        if filter:
            query = query.where(ChangeRoleRequest.request_status == filter)
        return query.slice(end-page_size, end).all()

    def is_has_change_role_messages(self, user_id):
        return bool(self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.user_id == user_id).first())

    def is_user_have_active_change_role_messages(self, user_id: int, count: int) -> bool:
        result = self.db.query(ChangeRoleRequest)\
            .filter(ChangeRoleRequest.user_id == user_id, ChangeRoleRequest.request_status == ChangeRoleRequestStatus.in_progress)\
            .limit(count).all()
        return len(result) == count

    def get_change_role_message(self, request_id):
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.id == request_id).first()

    def get_change_role_request_answer(self, request_id):
        return self.db.query(AnswerChangeRoleRequest).filter(AnswerChangeRoleRequest.request_id == request_id).first()

    def send_change_role_message_answer(self, request: ChangeRoleRequest, message: str, request_status: ChangeRoleRequestStatus, account_status: settings.UserTypeEnum):
        answer: AnswerChangeRoleRequest = request.answer
        user: User = request.user
        result_account_status = account_status if request_status == request_status.accepted else user.type
        user.type = result_account_status
        self.update(user)
        if not answer:
            answer = self.create(AnswerChangeRoleRequest(
                request_id=request.id,
                setted_account_status=result_account_status,
                message=message
            ))
        else:
            answer.message = message
            answer.setted_account_status = result_account_status
            self.update(answer)
        request.requested_account_status = account_status
        request.request_status = request_status
        self.update(request)
        return answer

    def get_not_answered_change_role_request_count(self):
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.request_status == ChangeRoleRequestStatus.in_progress).count()
