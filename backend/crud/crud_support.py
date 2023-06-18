from datetime import datetime
from backend.db.base import CRUDBase
from backend.models.slider import Slide
from backend.models.files import Image
from sqlalchemy.sql import or_
from backend.crud.crud_file import FileCruds
from backend.core.config import settings, env_config
from backend.models.support import SupportMessage, SupportMessageStatus, SupportMessageType


class SupportCrud(CRUDBase):
    def create_support_message(self, user_id: int, email: str, message: str, type: SupportMessageType) -> SupportMessage:
        return self.create(
            SupportMessage(
                user_id=user_id,
                email=email,
                message=message,
                type=type
            )
        )

    def get_message_by_id(self, message_id: int) -> SupportMessage:
        return self.db.query(SupportMessage).filter(SupportMessage.id == message_id).first()

    def get_messages(self, type: SupportMessageType, page: int = 1, page_size: int = int(env_config.get('SUPPORT_MESSAGES_PAGE_SIZE'))) -> list:
        end = page * page_size
        start = end - page_size
        query = self.db.query(SupportMessage)
        if type:
            query = query.filter(SupportMessage.type == type)
        return query.order_by(SupportMessage.created_at.desc()).slice(start, end).all()

    def update_support_message(self, db_message: SupportMessage, status: SupportMessageStatus) -> SupportMessage:
        db_message.status = status
        return self.update(db_message)
