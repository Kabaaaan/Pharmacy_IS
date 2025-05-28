from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()


from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse
from typing import List

from v1.schemas.schemas import PharmacyCreate, PharmacyResponse
from utils.auth import *
from servicies.pharmacy_service import PharmacyService

router = APIRouter()

@router.get('/', response_model=List[PharmacyResponse])
async def get_all_pharmacies():
    try:
        pharmacies = PharmacyService.get_all_pharmacies()
        return pharmacies
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get('/{id}', response_model=PharmacyResponse)
async def get_pharmacy_info_by_id(id: int):
    pharmacy = PharmacyService.get_pharmacy_by_id(id)
    if not pharmacy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacy not found"
        )
    return pharmacy

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pharmacy_by_id(id: int):
    success = PharmacyService.delete_pharmacy(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pharmacy not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post('/', response_model=PharmacyResponse, status_code=status.HTTP_201_CREATED)
async def create_pharmacy(pharmacy_data: PharmacyCreate):
    try:
        new_pharmacy = PharmacyService.create_pharmacy(
            address=pharmacy_data.address,
            phone_number=pharmacy_data.phone_number,
            schedule=pharmacy_data.schedule
        )
        return new_pharmacy
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )