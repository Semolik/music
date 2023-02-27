from backend.helpers.images import set_picture
from backend.models.clips import Clip
from backend.core.config import settings
import requests


def set_clip_data(clip: Clip):
    clip_obj = clip.as_dict()
    clip_obj['video'] = settings.SOCIAL_LINKS_FORMAT.get(
        'youtube_video').format(clip.video_id)
    return set_picture(clip_obj, clip.picture)


def video_is_exists(video_id: str):
    check_url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}"
    return "Bad Request" != requests.get(check_url).text
