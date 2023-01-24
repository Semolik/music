from backend.core.config import settings
from backend.crud.crud_musician import MusicianCrud
from backend.crud.crud_user import UserCruds
from backend.db.db import get_db
from sqlalchemy.orm import Session
from backend.crud.crud_clips import ClipsCruds
from backend.helpers.images import set_picture
from backend.helpers.clips import set_clip_data
from backend.helpers.music import set_album_info


def get_public_profile_as_dict(db: Session, user_id: int = None, public_profile_id: int = None, full_links=False,):
    db_public_profile = UserCruds(db).get_public_profile(
        user_id=user_id) if user_id else UserCruds(db).get_public_profile_by_id(id=public_profile_id)
    if not db_public_profile:
        return
    return get_public_profile_data(db_public_profile=db_public_profile, full_links=full_links)


def get_public_profile_data(db_public_profile, full_links):
    public_profile_data = db_public_profile.as_dict()
    links = {}
    for key, value in db_public_profile.links.as_dict().items():
        baseUrl = settings.SOCIAL_LINKS_FORMAT.get(key)
        links[key] = ((baseUrl.format(value)
                      if baseUrl else value) if value else None) if full_links else value
    public_profile_data['links'] = links
    public_profile_data = set_picture(
        public_profile_data, db_public_profile.picture)
    return public_profile_data


def get_musician_profile_as_dict(db: Session, user_id: int = None, public_profile_id: int = None, full_links=False):
    db_public_profile = UserCruds(db).get_public_profile_by_id(
        id=public_profile_id)
    if not db_public_profile:
        return
    public_profile_data = get_public_profile_data(
        db_public_profile=db_public_profile,
        full_links=full_links
    )
    if user_id:
        public_profile_data['liked'] = MusicianCrud(db).musician_is_liked(
            musician_id=db_public_profile.id, user_id=user_id)
    else:
        public_profile_data['liked'] = None
    public_profile_data['clips'] = list(
        map(
            set_clip_data,
            ClipsCruds(db).get_musician_clips(
                musician_id=db_public_profile.id, page=1, page_size=3)
        )
    )
    albums = MusicianCrud(db).get_musician_albums(
        limit=4, musician_id=db_public_profile.id)
    public_profile_data['albums'] = [set_album_info(
        db_album=album) for album in albums]
    return public_profile_data


def set_musician_info(data: dict, public_profile_id: int, db: Session, user_id: int = None):
    data['musician'] = get_public_profile_as_dict(
        db=db, public_profile_id=public_profile_id, user_id=user_id)
    return data
