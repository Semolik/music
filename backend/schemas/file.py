from pydantic import BaseModel


class File(BaseModel):
    file_name: str
    user_id: int
    url: str
    original_file_name: str
