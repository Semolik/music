from pydantic import BaseModel
from user import PublicProfile



class UploadTrack(BaseModel):
    name: str
    album_id: int
    feat: str | None = None


class Track(UploadTrack):
    id: int
    artist: PublicProfile

class CreateAlbum(BaseModel):
    name: str
    artist: PublicProfile
