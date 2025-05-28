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

# --------------------------
# Pharmacy Related Models
# --------------------------


class PharmacyBase(BaseModel):
    address: str
    phone_number: str
    schedule: str

class PharmacyCreate(PharmacyBase):
    pass

class PharmacyResponse(PharmacyBase):
    id: int
    
    class Config:
        from_attributes = True

# --------------------------
# Worker Related Models
# --------------------------

class RoleBase(BaseModel):
    name: str

class RoleResponse(RoleBase):
    id: int
    
    class Config:
        from_attributes = True

class WorkerBase(BaseModel):
    role_id: int
    pharmacy_id: int
    FIO: str
    salary: float
    enter_date: date
    phone_number: str
    home_address: str

class WorkerCreate(WorkerBase):
    pass

class WorkerResponse(WorkerBase):
    id: int
    role: RoleResponse
    
    class Config:
        from_attributes = True

class WorkerContactInfoUpdate(BaseModel):
    phone_number: Optional[str] = None
    home_address: Optional[str] = None

class WorkerPharmacyUpdate(BaseModel):
    new_pharmacy_id: int


# --------------------------
# Recipe Related Models
# --------------------------

class RecipeCreate(BaseModel):
    doctor_name: str
    license_number: int
    client_name: str
    medicine_id: int
    issue_date: date