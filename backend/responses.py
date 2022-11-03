from backend.schemas.error import HTTP_401_UNAUTHORIZED, USER_NOT_FOUND, HTTPError
from fastapi import status
UNAUTHORIZED_401 = {status.HTTP_401_UNAUTHORIZED: {
    "model": HTTP_401_UNAUTHORIZED}}
NOT_FOUND_USER = {status.HTTP_404_NOT_FOUND: {"model": USER_NOT_FOUND}}
