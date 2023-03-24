from typing import List
from backend.db.base import CRUDBase
from backend.core.config import settings
from backend.models.user import User
from backend.models.roles import AnswerChangeRoleRequest, ChangeRoleRequest, ChangeRoleRequestStatus


class ChangeRolesCruds(CRUDBase):
    def send_change_role_message(self, user_id, message, files) -> ChangeRoleRequest:
        db_change_role_request = ChangeRoleRequest(
            files=files,
            message=message,
            user_id=user_id
        )
        return self.create(db_change_role_request)

    def get_all_change_role_messages(self, page: int = 1, filter: ChangeRoleRequestStatus = None, page_size: int = settings.CHANGE_ROLE_PAGE_ITEMS) -> List[ChangeRoleRequest]:
        end = page * page_size
        query = self.db.query(ChangeRoleRequest).order_by(
            ChangeRoleRequest.id.desc())
        if filter:
            query = query.where(ChangeRoleRequest.request_status == filter)
        return query.slice(end-page_size, end).all()

    def get_user_change_role_messages(self, user_id, page: int, page_size: int = settings.CHANGE_ROLE_PAGE_ITEMS):

        end = page * page_size
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.user_id == user_id).order_by(ChangeRoleRequest.id.desc()).slice(end-page_size, end).all()

    def get_current_user_change_role_message(self, user_id):
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.user_id == user_id, ChangeRoleRequest.request_status == ChangeRoleRequestStatus.in_progress).first()

    def is_has_change_role_messages(self, user_id):
        return bool(self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.user_id == user_id).first())

    def user_have_active_change_role_request(self, user_id: int) -> bool:
        result = self.db.query(ChangeRoleRequest)\
            .filter(ChangeRoleRequest.user_id == user_id, ChangeRoleRequest.request_status == ChangeRoleRequestStatus.in_progress)\
            .first()
        return result is not None

    def user_have_change_role_request(self, user_id: int) -> bool:
        result = self.db.query(ChangeRoleRequest)\
            .filter(ChangeRoleRequest.user_id == user_id)\
            .first()
        return result is not None

    def get_change_role_message(self, request_id) -> ChangeRoleRequest:
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.id == request_id).first()

    def send_change_role_message_answer(self, request: ChangeRoleRequest, message: str, request_status: ChangeRoleRequestStatus):
        answer: AnswerChangeRoleRequest = request.answer
        user: User = request.user
        if request_status == ChangeRoleRequestStatus.accepted:
            user.type = settings.UserTypeEnum.musician
        elif request_status == ChangeRoleRequestStatus.rejected:
            user.type = settings.UserTypeEnum.user
        self.update(user)
        if not answer:
            answer = self.create(AnswerChangeRoleRequest(
                request_id=request.id,
                message=message
            ))
        else:
            answer.message = message
            self.update(answer)
        request.request_status = request_status
        self.update(request)
        return answer

    def get_not_answered_change_role_request_count(self):
        return self.db.query(ChangeRoleRequest).filter(ChangeRoleRequest.request_status == ChangeRoleRequestStatus.in_progress).count()
