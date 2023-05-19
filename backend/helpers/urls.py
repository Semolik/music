from uuid import UUID
from backend.core.config import settings


def get_track_url_by_id(track_id: UUID):
    return ''.join(
        [settings.API_V1_STR, '/tracks/', str(track_id), '/file'])
