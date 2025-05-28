from database.session import SessionLocal
from database.models import Supplier, AvailibleMedicineList, Shipment, Medicine
from sqlalchemy.exc import IntegrityError

class SupplierService:
    @staticmethod
    def create_supplier(name: str, additional_info: str = None, email: str = None, phone_number: str = None):
        db = SessionLocal()
        try:
            supplier = Supplier(
                name=name,
                additional_info=additional_info,
                email=email,
                phone_number=phone_number
            )
            db.add(supplier)
            db.commit()
            db.refresh(supplier)
            return supplier
        finally:
            db.close()

    @staticmethod
    def get_supplier_by_id(supplier_id: int):
        db = SessionLocal()
        try:
            return db.query(Supplier).filter(Supplier.id == supplier_id).first()
        finally:
            db.close()

    @staticmethod
    def get_all_suppliers():
        db = SessionLocal()
        try:
            return db.query(Supplier).all()
        finally:
            db.close()

    @staticmethod
    def add_medicine_to_supplier(supplier_id: int, medicine_id: int):
        db = SessionLocal()
        try:
            relation = AvailibleMedicineList(
                supplier_id=supplier_id,
                medicine_id=medicine_id
            )
            db.add(relation)
            db.commit()
            db.refresh(relation)
            return {
                "supplier_id": relation.supplier_id,
                "medicine_id": relation.medicine_id
            }
        except IntegrityError as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def get_supplier_medicines(supplier_id: int):
        db = SessionLocal()
        try:
            return db.query(AvailibleMedicineList).filter(
                AvailibleMedicineList.supplier_id == supplier_id
            ).all()
        finally:
            db.close()

    @staticmethod
    def delete_supplier(supplier_id: int):
        db = SessionLocal()
        try:
            has_shipments = db.query(Shipment).filter(
                Shipment.supplier_id == supplier_id
            ).first()
            
            if has_shipments:
                return False, "Supplier has shipments and cannot be deleted"
            
            supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
            if not supplier:
                return False, "Supplier not found"
                
            db.delete(supplier)
            db.commit()
            return True, "Supplier deleted successfully"
        except IntegrityError:
            db.rollback()
            return False, "Database error"
        finally:
            db.close()

    @staticmethod
    def get_supplier_with_medicines(supplier_id: int):
        db = SessionLocal()
        try:
            supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
            if not supplier:
                return None
            

            relations = db.query(AvailibleMedicineList).filter(
                AvailibleMedicineList.supplier_id == supplier_id
            ).all()
            
            medicines = []
            for rel in relations:
                medicine = db.query(Medicine).filter(Medicine.id == rel.medicine_id).first()
                if medicine:
                    medicines.append({
                        "id": medicine.id,
                        "name": medicine.name,
                        "price": medicine.price
                    })
            
            return {
                "name": supplier.name,
                'additional_info': supplier.additional_info,
                'email': supplier.email,
                'phone_number': supplier.phone_number,
                "medicines": medicines
            }
        finally:
            db.close()