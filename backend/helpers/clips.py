from backend.helpers.images import set_picture
from backend.models.music import Clip
from backend.core.config import settings


def set_clip_data(clip: Clip):
    clip_obj = clip.as_dict()
    clip_obj['video'] = settings.YOUTUBE_VIDEO.format(clip.video_id)
    return set_picture(clip_obj, clip.picture)
