from pydantic import BaseModel
from fastapi import Query


class File(BaseModel):
    file_name: str = Query(..., description="Имя файла")
    user_id: int = Query(..., description="ID пользователя")
    url: str = Query(..., description="Ссылка на файл")
    original_file_name: str = Query(
        ..., description="Имя файла, как оно было на компьютере пользователя")
