from pydantic import BaseModel


class File(BaseModel):
    file_name: str
    user_id: int
    type: str
    url: str
    original_file_name: str
