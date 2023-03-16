from datetime import datetime
from backend.db.base import CRUDBase
from backend.models.slider import Slide
from backend.models.files import Image


class SliderCrud(CRUDBase):
    def create_slide(self, name: str, picture: Image, url: str, is_active: bool, active_from: datetime = None, active_to: datetime = None, order: int = None):
        return self.create(
            Slide(
                name=name,
                picture=picture,
                url=url,
                is_active=is_active,
                active_from=active_from,
                active_to=active_to,
                order=order
            )
        )

    def get_slide_by_id(self, slide_id) -> Slide | None:
        return self.get(model=Slide, id=slide_id)
