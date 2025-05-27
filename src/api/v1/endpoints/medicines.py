# /medicine - CRUD для лекарств (Medicine)
# /medicine/needs_recipe - Лекарства, требующие рецепта


from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from api.v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()


from ...servicies.medicine_service import MedicineService