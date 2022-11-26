from backend.core.config import settings
from backend.crud.crud_music import music_crud
from backend.crud.crud_user import user_cruds
from backend.helpers.images import set_picture


def get_public_profile_as_dict(user_id: int = None, public_profile_id: int = None, full_links=False, liked_user_id: int = None):
    db_public_profile = user_cruds.get_public_profile(
        user_id=user_id) if user_id else user_cruds.get_public_profile_by_id(id=public_profile_id)
    if not db_public_profile:
        return
    public_profile_data = db_public_profile.as_dict()
    links = {}
    for key, value in db_public_profile.links.as_dict().items():
        baseUrl = settings.SOCIAL_LINKS_FORMAT.get(key)
        links[key] = ((baseUrl.format(value)
                      if baseUrl else value) if value else None) if full_links else value
    public_profile_data['links'] = links
    if liked_user_id and db_public_profile.user.is_musician:
        public_profile_data['liked'] = music_crud.musician_is_liked(
            musician_id=db_public_profile.id, user_id=liked_user_id)
    public_profile_data = set_picture(
        public_profile_data, db_public_profile.picture)
    return public_profile_data
