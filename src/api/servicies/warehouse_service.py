from database.session import SessionLocal
from database.models import WareHouse, ShipmentItems

class WarehouseService:
    @staticmethod
    def add_to_warehouse(shipment_item_id: int, count: int):
        db = SessionLocal()
        try:
            existing = db.query(WareHouse).filter(
                WareHouse.shipment_item_id == shipment_item_id
            ).first()
            
            if existing:
                existing.count += count
            else:
                warehouse_item = WareHouse(
                    shipment_item_id=shipment_item_id,
                    count=count
                )
                db.add(warehouse_item)
            
            db.commit()
        finally:
            db.close()

    @staticmethod
    def get_warehouse_items():
        db = SessionLocal()
        try:
            return db.query(WareHouse).all()
        finally:
            db.close()