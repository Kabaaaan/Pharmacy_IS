from typing import List, Dict
from datetime import date
from database.session import SessionLocal
from database.models import Shipment, ShipmentItems

class ShipmentService:
    @staticmethod
    def create_shipment(supplier_id: int, date: date = None, comment: str = None, invoice: str = None):
        db = SessionLocal()
        try:
            if date is None:
                date = date.today()
                
            shipment = Shipment(
                supplier_id=supplier_id,
                date=date,
                comment=comment,
                invoice=invoice
            )
            db.add(shipment)
            db.commit()
            db.refresh(shipment)
            return shipment
        finally:
            db.close()

    @staticmethod
    def add_item_to_shipment(
        shipment_id: int,
        medicine_id: int,
        count: int,
        best_before_date: date
    ):
        db = SessionLocal()
        try:
            item = ShipmentItems(
                shipment_id=shipment_id,
                medicine_id=medicine_id,
                count=count,
                best_before_date=best_before_date
            )
            db.add(item)
            db.commit()
            db.refresh(item)
            return item
        finally:
            db.close()

    @staticmethod
    def get_shipment_by_id(shipment_id: int):
        db = SessionLocal()
        try:
            return db.query(Shipment).filter(Shipment.id == shipment_id).first()
        finally:
            db.close()

    @staticmethod
    def get_shipment_items(shipment_id: int):
        db = SessionLocal()
        try:
            return db.query(ShipmentItems).filter(
                ShipmentItems.shipment_id == shipment_id
            ).all()
        finally:
            db.close()

    @staticmethod
    def create_shipment_with_items(
        supplier_id: int,
        items: List[Dict],
        invoice: str = None,
        comment: str = None
    ):
        db = SessionLocal()
        try:
            shipment = Shipment(
                supplier_id=supplier_id,
                date=date.today(),
                comment=comment,
                invoice=invoice
            )
            db.add(shipment)
            db.commit()
            db.refresh(shipment)
            
            for item in items:
                shipment_item = ShipmentItems(
                    shipment_id=shipment.id,
                    medicine_id=item['medicine_id'],
                    count=item['count'],
                    best_before_date=item['best_before_date']
                )
                db.add(shipment_item)
            
            db.commit()
            return shipment
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()