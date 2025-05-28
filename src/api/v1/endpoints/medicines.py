from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()


from servicies.medicine_service import MedicineService
from sqlalchemy.exc import IntegrityError


@router.get("/", response_model=List[MedicineResponse])
async def get_all_medicines():
    try:
        medicines = MedicineService.get_all_medicines()
        return medicines
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка лекарств: {str(e)}"
        )

@router.get("/{medicine_id}", response_model=MedicineResponse)
async def get_medicine(medicine_id: int):
    medicine = MedicineService.get_medicine_by_id(medicine_id)
    if not medicine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Лекарство не найдено"
        )
    return medicine

@router.post("/", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
async def create_medicine(medicine_data: MedicineCreate):
    try:
        medicine = MedicineService.create_medicine(
            name=medicine_data.name,
            price=medicine_data.price,
            description=medicine_data.description,
            need_recipe=medicine_data.need_recipe
        )
        return medicine
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Лекарство с таким названием уже существует"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании лекарства: {str(e)}"
        )