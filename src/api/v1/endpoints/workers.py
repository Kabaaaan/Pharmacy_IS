# /worker - CRUD для сотрудников (Worker)
# /worker/role - CRUD для ролей (Role)
# /worker/{id}/pharmacy - Получить аптеку сотрудника


from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from api.v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()