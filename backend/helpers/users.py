from backend.crud.crud_user import user_cruds
from backend.helpers.images import set_picture


def get_public_profile_as_dict(user_id: int = None, musician_id: int = None):
    db_public_profile = user_cruds.get_public_profile(
        user_id=user_id) if user_id else user_cruds.get_public_profile_by_id(id=musician_id)
    public_profile_data = db_public_profile.as_dict()
    public_profile_data['links'] = db_public_profile.links.as_dict()
    public_profile_data = set_picture(
        public_profile_data, db_public_profile.picture)
    return public_profile_data
