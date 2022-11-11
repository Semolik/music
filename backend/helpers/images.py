
from backend.models.user import File
# import models.user as user_models
from backend.core.config import settings



def set_picture(data: dict, picture: File):
    if picture:
        data['picture'] = ''.join(
            [settings.SERVER_LINK, settings.API_V1_STR,  settings.UPLOADS_ROUTE, '/images/', picture.file_name])
    return data
