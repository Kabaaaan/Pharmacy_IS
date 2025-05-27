# /report/sales - Отчет по продажам
# /report/financial - Финансовый отчет


from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()