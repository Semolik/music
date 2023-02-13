from backend.crud.crud_file import FileCruds
from backend.db.base import CRUDBase
from backend.core.config import env_config
from backend.models.files import Image
from backend.models.clips import Clip


class ClipsCruds(CRUDBase):
    def get_musician_clips(self, musician_id: int, page: int = 1, page_size: int = int(env_config.get('VITE_CLIP_PAGE_COUNT'))) -> list[Clip]:
        end = page * page_size
        return self.db.query(Clip).filter(Clip.musician_id == musician_id).slice(end-page_size, end).all()

    def create_clip(self, musician_id: int,  name: str, video_id: str, image_model: Image):
        return self.create(
            Clip(
                musician_id=musician_id,
                picture=image_model,
                name=name,
                video_id=video_id
            )
        )

    def update_clip(self, db_clip: Clip, name: str, video_id: str, image: Image):
        db_clip.name = name
        db_clip.video_id = video_id
        if image:
            FileCruds(self.db).replace_old_picture(
                model=db_clip, new_picture=image)
        return self.create(db_clip)

    def get_clip_by_id(self, clip_id: int) -> Clip | None:
        return self.db.query(Clip).filter(Clip.id == clip_id).first()
