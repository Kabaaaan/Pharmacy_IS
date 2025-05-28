from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse
from typing import List

from v1.schemas.schemas import *
from utils.auth import *
from servicies.worker_service import WorkerService, RoleService
from sqlalchemy.exc import IntegrityError

router = APIRouter()


@router.get('/role', response_model=List[RoleResponse])
async def get_all_roles():
    try:
        return RoleService.get_all_roles()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get('/', response_model=List[WorkerResponse])
async def get_all_workers():
    try:
        return WorkerService.get_all_workers()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get('/{id}', response_model=WorkerResponse)
async def get_worker_by_id(id: int):
    worker = WorkerService.get_worker_by_id(id)
    if not worker:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Worker not found"
        )
    return worker

@router.put('/{id}', response_model=WorkerResponse)
async def update_worker_contact_info(
    id: int, 
    contact_info: WorkerContactInfoUpdate
):
    try:
        worker = WorkerService.update_worker_contact_info(
            worker_id=id,
            phone_number=contact_info.phone_number,
            home_address=contact_info.home_address
        )
        if not worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found"
            )
        return worker
    
    except IntegrityError as e:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Worker might already exist but returning success status"}
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put('/work_place/{id}', response_model=WorkerResponse)
async def update_worker_pharmacy(
    id: int, 
    pharmacy_update: WorkerPharmacyUpdate
):
    try:
        worker = WorkerService.update_worker_pharmacy(
            worker_id=id,
            new_pharmacy_id=pharmacy_update.new_pharmacy_id
        )
        if not worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found"
            )
        return worker
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get('/work_place/{pharmacy_id}', response_model=List[WorkerResponse])
async def get_worker_by_pharmacy(pharmacy_id: int):
    workers = WorkerService.get_workers_by_pharmacy(pharmacy_id)
    if not workers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No workers found for this pharmacy"
        )
    return workers

@router.post('/', response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
async def create_worker(worker_data: WorkerCreate):
    try:
        new_worker = WorkerService.create_worker(
            role_id=worker_data.role_id,
            pharmacy_id=worker_data.pharmacy_id,
            FIO=worker_data.FIO,
            salary=worker_data.salary,
            enter_date=worker_data.enter_date,
            phone_number=worker_data.phone_number,
            home_address=worker_data.home_address
        )
        return new_worker
    
    except IntegrityError as e:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Worker might already exist but returning success status"}
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_worker(id: int):
    try:
        success = WorkerService.delete_worker(id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Worker not found"
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete worker as they are referenced in orders"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )