from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .session import Base  

Base = declarative_base()

class Doctor(Base):
    __tablename__ = 'doctor'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    license_number = Column(Integer, unique=True, nullable=False)
    
    recipes = relationship("Recipe", back_populates="doctor")

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    recipes = relationship("Recipe", back_populates="client")

class Medicine(Base):
    __tablename__ = 'medicine'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text)
    need_recipe = Column(Boolean, default=False, nullable=False)
    
    recipes = relationship("Recipe", back_populates="medicine")
    available_suppliers = relationship("Supplier", secondary="availible_medicine_list", back_populates="available_medicines")
    shipment_items = relationship("ShipmentItems", back_populates="medicine")
    order_items = relationship("OrderItems", back_populates="medicine")

class Supplier(Base):
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    additional_info = Column(Text)
    email = Column(String(100))
    phone_number = Column(String(20))
    
    available_medicines = relationship("Medicine", secondary="availible_medicine_list", back_populates="available_suppliers")
    shipments = relationship("Shipment", back_populates="supplier")

class AvailibleMedicineList(Base):
    __tablename__ = 'availible_medicine_list'
    supplier_id = Column(Integer, ForeignKey('supplier.id'), primary_key=True)
    medicine_id = Column(Integer, ForeignKey('medicine.id'), primary_key=True)

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctor.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('client.id'), nullable=False)
    medicine_id = Column(Integer, ForeignKey('medicine.id'), nullable=False)
    issue_date = Column(Date, nullable=False)
    
    doctor = relationship("Doctor", back_populates="recipes")
    client = relationship("Client", back_populates="recipes")
    medicine = relationship("Medicine", back_populates="recipes")
    order_items = relationship("OrderItems", back_populates="recipe")

class Shipment(Base):
    __tablename__ = 'shipment'
    id = Column(Integer, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('supplier.id'), nullable=False)
    date = Column(Date, nullable=False)
    comment = Column(Text)
    invoice = Column(String(100))
    
    supplier = relationship("Supplier", back_populates="shipments")
    items = relationship("ShipmentItems", back_populates="shipment")

class ShipmentItems(Base):
    __tablename__ = 'shipment_items'
    id = Column(Integer, primary_key=True)
    shipment_id = Column(Integer, ForeignKey('shipment.id'), nullable=False)
    medicine_id = Column(Integer, ForeignKey('medicine.id'), nullable=False)
    count = Column(Integer, nullable=False)
    best_before_date = Column(Date, nullable=False)
    
    shipment = relationship("Shipment", back_populates="items")
    medicine = relationship("Medicine", back_populates="shipment_items")
    warehouse_items = relationship("WareHouse", back_populates="shipment_item")
    stock_items = relationship("Stock", back_populates="shipment_item")

class WareHouse(Base):
    __tablename__ = 'ware_house'
    id = Column(Integer, primary_key=True)
    shipment_item_id = Column(Integer, ForeignKey('shipment_items.id'), nullable=False)
    count = Column(Integer, nullable=False)
    
    shipment_item = relationship("ShipmentItems", back_populates="warehouse_items")

class Pharmacy(Base):
    __tablename__ = 'pharmacy'
    id = Column(Integer, primary_key=True)
    address = Column(String(200), nullable=False)
    phone_number = Column(String(20), nullable=False)
    schedule = Column(String(100), nullable=False)
    
    workers = relationship("Worker", back_populates="pharmacy")
    stocks = relationship("Stock", back_populates="pharmacy")

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    
    workers = relationship("Worker", back_populates="role")

class Worker(Base):
    __tablename__ = 'worker'
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('pharmacy.id'), nullable=False)
    FIO = Column(String(150), nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    enter_date = Column(Date, nullable=False)
    phone_number = Column(String(20), nullable=False)
    home_address = Column(String(200), nullable=False)
    
    role = relationship("Role", back_populates="workers")
    pharmacy = relationship("Pharmacy", back_populates="workers")
    orders = relationship("Order", back_populates="pharmacist")

class TypePay(Base):
    __tablename__ = 'type_pay'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    additional_info = Column(Text)
    
    orders = relationship("Order", back_populates="type_pay")

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    type_pay_id = Column(Integer, ForeignKey('type_pay.id'), nullable=False)
    pharmacist_id = Column(Integer, ForeignKey('worker.id'), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, nullable=False)
    
    type_pay = relationship("TypePay", back_populates="orders")
    pharmacist = relationship("Worker", back_populates="orders")
    items = relationship("OrderItems", back_populates="order")

class OrderItems(Base):
    __tablename__ = 'order_items'
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    medicine_id = Column(Integer, ForeignKey('medicine.id'), primary_key=True)
    stock_id = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    
    order = relationship("Order", back_populates="items")
    medicine = relationship("Medicine", back_populates="order_items")
    stock = relationship("Stock", back_populates="order_items")
    recipe = relationship("Recipe", back_populates="order_items")

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    shipment_item_id = Column(Integer, ForeignKey('shipment_items.id'), nullable=False)
    pharmacy_id = Column(Integer, ForeignKey('pharmacy.id'), nullable=False)
    count = Column(Integer, nullable=False)
    
    shipment_item = relationship("ShipmentItems", back_populates="stock_items")
    pharmacy = relationship("Pharmacy", back_populates="stocks")
    order_items = relationship("OrderItems", back_populates="stock")

class Delivery(Base):
    __tablename__ = 'delivery'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    
    items = relationship("DeliveryItems", back_populates="delivery")

class DeliveryItems(Base):
    __tablename__ = 'delivery_items'
    delivery_id = Column(Integer, ForeignKey('delivery.id'), primary_key=True)
    stock_id = Column(Integer, ForeignKey('stock.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    
    delivery = relationship("Delivery", back_populates="items")
    stock = relationship("Stock")