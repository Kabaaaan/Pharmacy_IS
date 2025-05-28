from database.session import SessionLocal
from database.models import Worker, Role
from sqlalchemy.orm import joinedload


class RoleService:
    @staticmethod
    def create_role(name: str):
        db = SessionLocal()
        try:
            role = Role(name=name)
            db.add(role)
            db.commit()
            db.refresh(role)
            return role
        finally:
            db.close()

    @staticmethod
    def delete_role(role_id: int):
        db = SessionLocal()
        try:
            role = db.query(Role).filter(Role.id == role_id).first()
            if role:
                db.delete(role)
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def get_all_roles():
        db = SessionLocal()
        try:
            return db.query(Role).all()
        finally:
            db.close()

    @staticmethod
    def get_role_by_id(role_id: int):
        db = SessionLocal()
        try:
            return db.query(Role).filter(Role.id == role_id).first()
        finally:
            db.close()

class WorkerService:
    @staticmethod
    def create_worker(role_id: int, pharmacy_id: int, FIO: str, salary: float, 
                     enter_date: str, phone_number: str, home_address: str):
        db = SessionLocal()
        try:
            worker = Worker(
                role_id=role_id,
                pharmacy_id=pharmacy_id,
                FIO=FIO,
                salary=salary,
                enter_date=enter_date,
                phone_number=phone_number,
                home_address=home_address
            )
            db.add(worker)
            db.commit()
            db.refresh(worker)
            return worker
        finally:
            db.close()

    @staticmethod
    def delete_worker(worker_id: int):
        db = SessionLocal()
        try:
            worker = db.query(Worker).filter(Worker.id == worker_id).first()
            if worker:
                db.delete(worker)
                db.commit()
                return True
            return False
        finally:
            db.close()

    @staticmethod
    def get_all_workers():
        db = SessionLocal()
        try:
            return db.query(Worker).options(joinedload(Worker.role)).all()
        finally:
            db.close()

    @staticmethod
    def get_worker_by_id(worker_id: int):
        db = SessionLocal()
        try:
            return db.query(Worker).options(joinedload(Worker.role)).filter(Worker.id == worker_id).first()
        finally:
            db.close()

    @staticmethod
    def get_workers_by_pharmacy(pharmacy_id: int):
        db = SessionLocal()
        try:
            return db.query(Worker).options(joinedload(Worker.role)).filter(Worker.pharmacy_id == pharmacy_id).all()
        finally:
            db.close()

    @staticmethod
    def update_worker_contact_info(worker_id: int, phone_number: str = None, home_address: str = None):
        db = SessionLocal()
        try:
            worker = db.query(Worker).filter(Worker.id == worker_id).first()
            if not worker:
                return None
                
            if phone_number is not None:
                worker.phone_number = phone_number
            if home_address is not None:
                worker.home_address = home_address
                
            db.commit()
            db.refresh(worker)
            return worker
        finally:
            db.close()

    @staticmethod
    def update_worker_pharmacy(worker_id: int, new_pharmacy_id: int):
        db = SessionLocal()
        try:
            worker = db.query(Worker).filter(Worker.id == worker_id).first()
            if not worker:
                return None
                
            worker.pharmacy_id = new_pharmacy_id
            db.commit()
            db.refresh(worker)
            return worker
        finally:
            db.close()
