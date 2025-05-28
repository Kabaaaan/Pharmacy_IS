from database.session import SessionLocal
from database.models import Pharmacy


class PharmacyService:
    @staticmethod
    def create_pharmacy(address: str, phone_number: str, schedule: str):
        db = SessionLocal()
        try:
            pharmacy = Pharmacy(
                address=address,
                phone_number=phone_number,
                schedule=schedule
            )
            db.add(pharmacy)
            db.commit()
            db.refresh(pharmacy)
            return pharmacy
        finally:
            db.close()

    @staticmethod
    def delete_pharmacy(pharmacy_id: int):
        db = SessionLocal()
        try:
            pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()
            if pharmacy:
                db.delete(pharmacy)
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def get_all_pharmacies():
        db = SessionLocal()
        try:
            return db.query(Pharmacy).all()
        finally:
            db.close()

    @staticmethod
    def get_pharmacy_by_id(pharmacy_id: int):
        db = SessionLocal()
        try:
            return db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()
        finally:
            db.close()