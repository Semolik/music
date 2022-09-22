from fastapi import APIRouter
from .endpoints import login, logout, signup

api_v1_router = APIRouter()
api_v1_router.include_router(login.router)
api_v1_router.include_router(logout.router)
api_v1_router.include_router(signup.router)
