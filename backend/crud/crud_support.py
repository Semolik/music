from datetime import datetime
from backend.db.base import CRUDBase
from backend.models.slider import Slide
from backend.models.files import Image
from sqlalchemy.sql import or_
from backend.crud.crud_file import FileCruds
from backend.core.config import settings
from backend.models.support import SupportMessage


class SupportCrud(CRUDBase):
    def create_support_message(self, user_id: int, email: str, message: str):
        return self.create(
            SupportMessage(
                user_id=user_id,
                email=email,
                message=message
            )
        )

    def get_message_by_id(self, message_id: int) -> SupportMessage:
        return self.db.query(SupportMessage).filter(SupportMessage.id == message_id).first()
