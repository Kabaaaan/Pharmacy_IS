# /auth/login - Вход в систему
# /auth/refresh - Обновление токена
# /auth/me - Информация о текущем пользователе


from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from api.v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()