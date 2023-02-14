from pydantic import BaseModel


class LikesInfo(BaseModel):
    likes_count: int
    liked: bool
