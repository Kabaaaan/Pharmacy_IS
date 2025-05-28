from database.session import SessionLocal
from database.models import Recipe, Doctor, Client, Medicine
from datetime import date
from database.models import Order

class RecipeService:
    @staticmethod
    def create_recipe(doctor_name: str, license_number: int, 
                    client_name: str, medicine_id: int, 
                    issue_date: date):
        db = SessionLocal()
        try:
            medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
            if not medicine:
                raise ValueError("Medicine not found")
            
            doctor = db.query(Doctor).filter(Doctor.license_number == license_number).first()
            if not doctor:
                doctor = Doctor(name=doctor_name, license_number=license_number)
                db.add(doctor)
                db.commit()
                db.refresh(doctor)
            
            client = db.query(Client).filter(Client.name == client_name).first()
            if not client:
                client = Client(name=client_name)
                db.add(client)
                db.commit()
                db.refresh(client)
            
            recipe = Recipe(
                doctor_id=doctor.id,
                client_id=client.id,
                medicine_id=medicine_id,
                issue_date=issue_date
            )
            db.add(recipe)
            db.commit()
            db.refresh(recipe)
            return recipe
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def get_all_recipes():
        db = SessionLocal()
        try:
            recipes = db.query(
                Recipe,
                Medicine.name.label('medicine_name'),
                Doctor.name.label('doctor_name'),
                Client.name.label('client_name')
            ).join(
                Medicine, Recipe.medicine_id == Medicine.id
            ).join(
                Doctor, Recipe.doctor_id == Doctor.id
            ).join(
                Client, Recipe.client_id == Client.id
            ).all()
            
            return [{
                "id": recipe.Recipe.id,
                "issue_date": recipe.Recipe.issue_date,
                "medicine_name": recipe.medicine_name,
                "doctor_name": recipe.doctor_name,
                "client_name": recipe.client_name
            } for recipe in recipes]
        finally:
            db.close()

    @staticmethod
    def delete_recipe(recipe_id: int):
        db = SessionLocal()
        try:
            recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
            if not recipe:
                return False
            
            db.delete(recipe)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    @staticmethod
    def get_recipe_by_id(recipe_id: int):
        db = SessionLocal()
        try:
            recipe = db.query(
                Recipe,
                Medicine.name.label('medicine_name'),
                Doctor.name.label('doctor_name'),
                Client.name.label('client_name')
            ).join(
                Medicine, Recipe.medicine_id == Medicine.id
            ).join(
                Doctor, Recipe.doctor_id == Doctor.id
            ).join(
                Client, Recipe.client_id == Client.id
            ).filter(
                Recipe.id == recipe_id
            ).first()
            
            if recipe:
                return {
                    "id": recipe.Recipe.id,
                    "issue_date": recipe.Recipe.issue_date,
                    "medicine_name": recipe.medicine_name,
                    "doctor_name": recipe.doctor_name,
                    "client_name": recipe.client_name
                }
            return None
        finally:
            db.close()

    @staticmethod
    def get_recipes_by_date(min_date: date):
        db = SessionLocal()
        try:
            recipes = db.query(
                Recipe,
                Medicine.name.label('medicine_name'),
                Doctor.name.label('doctor_name'),
                Client.name.label('client_name')
            ).join(
                Medicine, Recipe.medicine_id == Medicine.id
            ).join(
                Doctor, Recipe.doctor_id == Doctor.id
            ).join(
                Client, Recipe.client_id == Client.id
            ).filter(
                Recipe.issue_date >= min_date
            ).all()
            
            return [{
                "id": recipe.Recipe.id,
                "issue_date": recipe.Recipe.issue_date,
                "medicine_name": recipe.medicine_name,
                "doctor_name": recipe.doctor_name,
                "client_name": recipe.client_name
            } for recipe in recipes]
        finally:
            db.close()


class OrderService:
    @staticmethod
    def get_orders_after_date(start_date: date):
        db = SessionLocal()
        try:
            return db.query(Order).filter(Order.date >= start_date).all()
        finally:
            db.close()

    @staticmethod
    def get_order_summary_after_date(start_date: date):
        db = SessionLocal()
        try:
            orders = db.query(Order).filter(Order.date >= start_date).all()
            total_count = len(orders)
            total_price = sum(order.total_price for order in orders)
            return total_count, total_price
        finally:
            db.close()