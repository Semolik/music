from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from backend.schemas.file import ImageLink
from backend.helpers.forms import ValidateJsonWithFormBody


class SlideBase(BaseModel):
    name: str
    is_active: bool
    active_from: datetime | None
    active_to: datetime | None
    order: int | None
    url: str | None


class CreateSlide(SlideBase, ValidateJsonWithFormBody):
    ...


class Slide(SlideBase):
    id: UUID
    picture: ImageLink

    class Config:
        orm_mode = True
