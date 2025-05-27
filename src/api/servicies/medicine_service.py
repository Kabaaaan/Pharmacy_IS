from database.session import SessionLocal
from database.models import Medicine

class MedicineService:
    @staticmethod
    def create_medicine(name: str, price: float, description: str = None, need_recipe: bool = False):
        db = SessionLocal()
        try:
            medicine = Medicine(
                name=name,
                price=price,
                description=description,
                need_recipe=need_recipe
            )
            db.add(medicine)
            db.commit()
            db.refresh(medicine)
            return medicine
        finally:
            db.close()

    @staticmethod
    def get_medicine_by_id(medicine_id: int):
        db = SessionLocal()
        try:
            return db.query(Medicine).filter(Medicine.id == medicine_id).first()
        finally:
            db.close()

    @staticmethod
    def get_all_medicines():
        db = SessionLocal()
        try:
            return db.query(Medicine).all()
        finally:
            db.close()