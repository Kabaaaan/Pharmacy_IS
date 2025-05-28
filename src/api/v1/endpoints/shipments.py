from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List

from v1.schemas.schemas import *
from utils.auth import *

from servicies.supplier_service import SupplierService
from servicies.shipment_service import ShipmentService
from servicies.medicine_service import MedicineService

router = APIRouter()


@router.get('/supplier', response_model=List[SupplierResponse])
async def get_all_suppliers():
    suppliers = SupplierService.get_all_suppliers()
    return suppliers

@router.post('/supplier', response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
async def create_supplier(supplier_data: SupplierCreate):
    supplier = SupplierService.create_supplier(
        name=supplier_data.name,
        additional_info=supplier_data.additional_info,
        email=supplier_data.email,
        phone_number=supplier_data.phone_number
    )
    return supplier

@router.get("/supplier/{supplier_id}", response_model=SupplierWithMedicinesResponse)
async def get_supplier_with_medicines(supplier_id: int):
    result = SupplierService.get_supplier_with_medicines(supplier_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Поставщик не найден"
        )
    return result

@router.delete('/supplier/{supplier_id}')
async def delete_supplier(supplier_id: int):
    success, message = SupplierService.delete_supplier(supplier_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}


@router.post('/', response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(shipment_data: ShipmentCreate):
    medicines_info = []
    for item in shipment_data.items:
        medicine = MedicineService.get_medicine_by_id(item.medicine_id)
        medicines_info.append(f"{medicine.name} x{item.count}")
    
    invoice = " | ".join(medicines_info)
    
    shipment = ShipmentService.create_shipment_with_items(
        supplier_id=shipment_data.supplier_id,
        items=[item.dict() for item in shipment_data.items],
        invoice=invoice,
        comment=shipment_data.comment
    )
    return shipment


@router.post(
    "supplier/medicines",
    response_model=SupplierMedicineLinkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить лекарство к поставщику",
    description="Создает связь между поставщиком и лекарством в таблице доступных лекарств"
)
async def add_medicine_to_supplier(
    link_data: SupplierMedicineLinkCreate
): 
    try:
        relation = SupplierService.add_medicine_to_supplier(
            supplier_id=link_data.supplier_id,
            medicine_id=link_data.medicine_id
        )
        return relation
    except IntegrityError as e:
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Поставщик или лекарство не найдены"
            )
        elif "unique constraint" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Это лекарство уже добавлено к данному поставщику"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при добавлении лекарства к поставщику"
        )