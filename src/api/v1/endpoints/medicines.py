# /medicine - CRUD для лекарств (Medicine)
# /medicine/needs_recipe - Лекарства, требующие рецепта


from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()


from servicies.medicine_service import MedicineService


# @router.post('/medicine')
# async def create_medicine() -> JSONResponse:
#     medicne = MedicineService.create_medicine(name='Витамин Д3',
#                                               price=570,
#                                               description='БАД',
#                                               need_recipe=False)
#     return {'medicne': medicne}

# @router.get('/medicine')
# async def get_medicine() -> JSONResponse:
#     medicines = MedicineService.get_all_medicines()
#     return {'medicines': medicines}