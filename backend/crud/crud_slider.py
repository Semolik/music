from datetime import datetime
from backend.db.base import CRUDBase
from backend.models.slider import Slide
from backend.models.files import Image
from sqlalchemy.sql import or_
from backend.crud.crud_file import FileCruds


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

    def get_all(self, page: int = 1, page_size: int = 10) -> list[Slide]:
        end = page * page_size
        return self.db.query(Slide).order_by(Slide.order, Slide.active_from).slice(end - page_size, end).all()

    def get_slide_by_id(self, slide_id) -> Slide | None:
        return self.get(model=Slide, id=slide_id)

    def get_opened_slides(self) -> list[Slide]:
        return self.db.query(Slide).filter(
            or_(
                Slide.active_from.is_(None),
                Slide.active_from <= datetime.now(),
            ),
            or_(
                Slide.active_to.is_(None),
                Slide.active_to >= datetime.now(),
            ),
            Slide.is_active
        ).order_by(Slide.order).all()

    def update_slide(self, slide: Slide, name: str, picture: Image, url: str, is_active: bool, active_from: datetime = None, active_to: datetime = None, order: int = None):
        slide.name = name
        slide.url = url
        slide.is_active = is_active
        slide.active_from = active_from
        slide.active_to = active_to
        slide.order = order
        if picture:
            FileCruds(self.db).replace_old_picture(slide, picture)
        return self.update(slide)
