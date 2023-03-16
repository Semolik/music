from backend.crud.crud_slider import SliderCrud
from backend.schemas.slider import Slide, CreateSlide
from backend.helpers.images import save_image
from backend.helpers.auth_helper import Authenticate
from fastapi import Depends, APIRouter, HTTPException, Query, status, UploadFile, File


router = APIRouter(tags=['Слайдер'], prefix='/slider')


@router.post('', response_model=Slide)
def create_slide(
    slide: CreateSlide,
    slide_image: UploadFile = File(...),
    Auth: Authenticate = Depends(Authenticate(is_admin=True)),
):
    '''Создание слайда'''
    db_image = save_image(
        db=Auth.db,
        upload_file=slide_image,
        user_id=Auth.current_user_id,
        resize_image_options=(3000, 3000)
    )
    slider_crud = SliderCrud(db=Auth.db)
    return slider_crud.create_slide(
        name=slide.name,
        picture=db_image,
        url=slide.url,
        is_active=slide.is_active,
        active_from=slide.active_from,
        active_to=slide.active_to,
    )
