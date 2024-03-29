
from backend.db.base import CRUDBase
from backend.models.files import Image, File


class FileCruds(CRUDBase):

    def replace_old_picture(self, model, new_picture):
        picture: Image = model.picture
        model.picture = new_picture
        self.update(model)
        if picture:
            self.delete(picture)
        return model

    def create_image(self, height: int, width: int, user_id: int):
        return self.create(Image(height=height, width=width, user_id=user_id))

    def create_file(self, original_file_name: str, user_id: int, extension: str):
        return self.create(File(user_id=user_id, original_file_name=original_file_name, extension=extension))

    def get_image_by_id(self, image_id) -> Image | None:
        return self.get(model=Image, id=image_id)

    def get_file_by_id(self, file_id) -> File | None:
        return self.get(model=File, id=file_id)
