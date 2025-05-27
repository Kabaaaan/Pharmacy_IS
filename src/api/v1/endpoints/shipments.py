# /shipment/suppliers - CRUD для поставщиков (Supplier)
# /shipment/suppliers/{id}/medicines - Лекарства поставщика
# /shipment/suppliers/{id}/shipments - Поставки от поставщика

# /shipment/warehouse - Остатки на складе (WareHouse)
# /shipment Закупки (Shipment)
# /shipment/warehouse/shipments/{id}/items - Элементы закупки


from fastapi import APIRouter, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse

from api.v1.schemas.schemas import *
from utils.auth import *

router = APIRouter()