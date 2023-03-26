from uuid import UUID
from backend.crud.crud_slider import SliderCrud
from backend.helpers.files import valid_content_length
from backend.schemas.slider import Slide, CreateSlide
from backend.helpers.images import save_image
from backend.helpers.auth_helper import Authenticate
from fastapi import Depends, APIRouter, HTTPException, Query, status, UploadFile, File
from backend.core.config import settings


router = APIRouter(tags=['Слайдер'], prefix='/slider')


@router.post('', response_model=Slide, dependencies=[Depends(valid_content_length(settings.MAX_SLIDE_FILE_SIZE_MB))])
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
        order=slide.order,
    )


@router.get('', response_model=list[Slide])
def get_slides(
    Auth: Authenticate = Depends(Authenticate(required=False)),
):
    '''Получение всех слайдов'''
    slider_crud = SliderCrud(db=Auth.db)
    return slider_crud.get_opened_slides()


@router.get('/all', response_model=list[Slide])
def get_all_slides(
    page: int = Query(1, ge=1),
    Auth: Authenticate = Depends(Authenticate(is_admin=True)),
):
    '''Получение всех слайдов'''
    slider_crud = SliderCrud(db=Auth.db)
    return slider_crud.get_all(page=page)


@router.get('/{slide_id}', response_model=Slide)
def get_slide_by_id(
    slide_id: UUID,
    Auth: Authenticate = Depends(Authenticate(is_admin=True)),
):
    '''Получение слайда по id'''
    slider_crud = SliderCrud(db=Auth.db)
    slide = slider_crud.get_slide_by_id(slide_id)
    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Слайд не найден')
    return slide


@router.put('/{slide_id}', response_model=Slide, dependencies=[Depends(valid_content_length(settings.MAX_SLIDE_FILE_SIZE_MB))])
def update_slide(
    slide_id: UUID,
    slide: CreateSlide,
    slide_image: UploadFile = File(None),
    Auth: Authenticate = Depends(Authenticate(is_admin=True)),
):
    '''Обновление слайда'''
    slider_crud = SliderCrud(db=Auth.db)
    db_slide = slider_crud.get_slide_by_id(slide_id)
    if not db_slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Слайд не найден')
    db_image = save_image(
        db=Auth.db,
        upload_file=slide_image,
        user_id=Auth.current_user_id,
        resize_image_options=(3000, 3000)
    )

    return slider_crud.update_slide(
        slide=db_slide,
        name=slide.name,
        picture=db_image,
        url=slide.url,
        is_active=slide.is_active,
        active_from=slide.active_from,
        active_to=slide.active_to,
        order=slide.order,
    )


@router.delete('/{slide_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_slide(
    slide_id: UUID,
    Auth: Authenticate = Depends(Authenticate(is_admin=True)),
):
    '''Удаление слайда'''
    slider_crud = SliderCrud(db=Auth.db)
    slide = slider_crud.get_slide_by_id(slide_id)
    if not slide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Слайд не найден')
    slider_crud.delete(slide)
