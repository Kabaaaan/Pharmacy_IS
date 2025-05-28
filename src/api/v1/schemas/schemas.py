from datetime import date
from typing import List, Optional
from pydantic import BaseModel

# --------------------------
# Supplier Related Models
# --------------------------

class SupplierBase(BaseModel):
    name: str
    additional_info: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    id: int
    
    class Config:
        from_attributes = True

class SupplierWithMedicinesResponse(SupplierBase):
    medicines: List['MedicineShortResponse']

# --------------------------
# Medicine Related Models
# --------------------------

class MedicineBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    need_recipe: bool = False

class MedicineCreate(MedicineBase):
    pass

class MedicineResponse(MedicineBase):
    id: int
    
    class Config:
        from_attributes = True

class MedicineShortResponse(BaseModel):
    id: int
    name: str
    price: float
    
    class Config:
        from_attributes = True

# --------------------------
# Supplier-Medicine Link Models
# --------------------------

class SupplierMedicineLinkBase(BaseModel):
    supplier_id: int
    medicine_id: int

class SupplierMedicineLinkCreate(SupplierMedicineLinkBase):
    pass

class SupplierMedicineLinkResponse(SupplierMedicineLinkBase):
    class Config:
        from_attributes = True

# --------------------------
# Shipment Related Models
# --------------------------

class ShipmentItemCreate(BaseModel):
    medicine_id: int
    count: int
    best_before_date: date

class ShipmentCreate(BaseModel):
    supplier_id: int
    items: List[ShipmentItemCreate]
    comment: Optional[str] = None

class ShipmentResponse(BaseModel):
    id: int
    supplier_id: int
    date: date
    invoice: Optional[str] = None
    comment: Optional[str] = None
    
    class Config:
        from_attributes = True