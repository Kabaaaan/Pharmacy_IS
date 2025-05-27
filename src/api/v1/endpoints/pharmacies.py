# /pharmacy - CRUD для аптек (Pharmacy)
# /pharmacy/{id}/stock - Остатки в аптеке
# /pharmacy/{id}/workers - Сотрудники аптеки

# /pharmacy/{id}/stock/low - Лекарства с низким остатком
# /pharmacy/{id}/stock/expiring - Лекарства с истекающим сроком


from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()