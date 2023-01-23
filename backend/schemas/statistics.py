from pydantic import BaseModel
from fastapi import Query


class UsersStats(BaseModel):
    user_count: int = Query(..., description="Количество пользователей")
    admin_count: int = Query(..., description="Количество администраторов")
    change_role_request_count: int = Query(
        ..., description="Количество запросов на смену типа аккаунта")
    musician_count: int = Query(..., description="Количество музыкантов")
