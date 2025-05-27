from fastapi import APIRouter

from v1.endpoints.auth import router as auth_router
from v1.endpoints.workers import router as workers_router
from v1.endpoints.deliveries import router as deliveries_router
from v1.endpoints.medicines import router as medicines_router
from v1.endpoints.orders import router as orders_router
from v1.endpoints.pharmacies import router as pharmacies_router
from v1.endpoints.reports import router as reports_router
from v1.endpoints.shipments import router as shipments_router


api_router = APIRouter(prefix="/v1")

api_router.include_router(workers_router, prefix="/worker", tags=["workers"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(deliveries_router, prefix="/delivery", tags=["workers"])
api_router.include_router(medicines_router, prefix="/medicine", tags=["medicine"])
api_router.include_router(orders_router, prefix="/order", tags=["order"])
api_router.include_router(pharmacies_router, prefix="/pharmacy", tags=["pharmacy"])
api_router.include_router(reports_router, prefix="/report", tags=["report"])
api_router.include_router(shipments_router, prefix="/shipment", tags=["shipment"])
