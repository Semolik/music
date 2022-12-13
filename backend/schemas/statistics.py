from pydantic import BaseModel


class UsersStats(BaseModel):
    user_count: int
    admin_count: int
    change_role_request_count: int
    musician_count: int
