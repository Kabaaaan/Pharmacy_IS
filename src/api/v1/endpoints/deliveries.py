# /delivery - CRUD для поставок (Delivery)
# /delivery/{id}/items - Элементы поставки
# /delivery/to_pharmacy - Поставки в конкретную аптеку


from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()