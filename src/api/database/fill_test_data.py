from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from . import models  

def fill_database(session: Session):
    medicines = [
        models.Medicine(
            name="Аспирин", 
            price=Decimal("120.50"), 
            description="Обезболивающее", 
            need_recipe=False
        ),
        models.Medicine(
            name="Парацетамол", 
            price=Decimal("85.30"), 
            description="Жаропонижающее", 
            need_recipe=False
        ),
        models.Medicine(
            name="Ибупрофен", 
            price=Decimal("150.75"), 
            description="Противовоспалительное", 
            need_recipe=False
        ),
        models.Medicine(
            name="Амоксициллин", 
            price=Decimal("320.00"), 
            description="Антибиотик", 
            need_recipe=True
        ),
        models.Medicine(
            name="Лозартан", 
            price=Decimal("280.40"), 
            description="От давления", 
            need_recipe=True
        ),
        models.Medicine(
            name="Метформин", 
            price=Decimal("195.60"), 
            description="При диабете", 
            need_recipe=True
        ),
        models.Medicine(
            name="Сальбутамол", 
            price=Decimal("410.20"), 
            description="Ингалятор", 
            need_recipe=True
        ),
        models.Medicine(
            name="Омепразол", 
            price=Decimal("220.80"), 
            description="Для ЖКТ", 
            need_recipe=False
        ),
        models.Medicine(
            name="Цитрамон", 
            price=Decimal("95.25"), 
            description="От головной боли", 
            need_recipe=False
        ),
        models.Medicine(
            name="Валерьянка", 
            price=Decimal("65.40"), 
            description="Успокоительное", 
            need_recipe=False
        ),
        models.Medicine(
            name="Лоратадин", 
            price=Decimal("180.90"), 
            description="Антигистаминное", 
            need_recipe=False
        ),
        models.Medicine(
            name="Анальгин", 
            price=Decimal("110.30"), 
            description="Обезболивающее", 
            need_recipe=False
        ),
        models.Medicine(
            name="Називин", 
            price=Decimal("145.50"), 
            description="Капли в нос", 
            need_recipe=False
        ),
        models.Medicine(
            name="Фенистил", 
            price=Decimal("320.75"), 
            description="От аллергии", 
            need_recipe=False
        ),
        models.Medicine(
            name="Нурофен", 
            price=Decimal("210.00"), 
            description="Обезболивающее", 
            need_recipe=False
        )
    ]
    session.add_all(medicines)
    session.commit()

    roles = [
        models.Role(name="Фармацевт"),
        models.Role(name="Администратор"),
        models.Role(name="Менеджер по продажам"),
        models.Role(name="Менеджер по закупкам")
    ]
    session.add_all(roles)
    session.commit()

    pharmacies = [
        models.Pharmacy(
            address="ул. Ленина, д. 15", 
            phone_number="+79151234567", 
            schedule="9:00-21:00"
        ),
        models.Pharmacy(
            address="пр. Мира, д. 42", 
            phone_number="+79157654321", 
            schedule="8:00-22:00"
        ),
        models.Pharmacy(
            address="ул. Гагарина, д. 7", 
            phone_number="+79159876543", 
            schedule="10:00-20:00"
        ),
        models.Pharmacy(
            address="ул. Пушкина, д. 23", 
            phone_number="+79153215476", 
            schedule="8:30-21:30"
        ),
        models.Pharmacy(
            address="пр. Строителей, д. 18", 
            phone_number="+79158765432", 
            schedule="9:00-20:00"
        )
    ]
    session.add_all(pharmacies)
    session.commit()

    workers = [
        models.Worker(
            role_id=roles[0].id, pharmacy_id=pharmacies[0].id,
            FIO="Иванова Анна Петровна", salary=Decimal("45000.00"),
            enter_date=date(2022, 1, 15), phone_number="+79161111111",
            home_address="ул. Садовая, д.1"
        ),
        models.Worker(
            role_id=roles[0].id, pharmacy_id=pharmacies[0].id,
            FIO="Петрова Елена Владимировна", salary=Decimal("47000.00"),
            enter_date=date(2022, 3, 10), phone_number="+79162222222",
            home_address="ул. Лесная, д.5"
        ),
        models.Worker(
            role_id=roles[0].id, pharmacy_id=pharmacies[1].id,
            FIO="Сидорова Ольга Игоревна", salary=Decimal("46000.00"),
            enter_date=date(2021, 11, 20), phone_number="+79163333333",
            home_address="пр. Парковый, д.12"
        ),
        models.Worker(
            role_id=roles[0].id, pharmacy_id=pharmacies[1].id,
            FIO="Кузнецов Дмитрий Алексеевич", salary=Decimal("48000.00"),
            enter_date=date(2023, 2, 5), phone_number="+79164444444",
            home_address="ул. Центральная, д.7"
        ),
        models.Worker(
            role_id=roles[0].id, pharmacy_id=pharmacies[2].id,
            FIO="Васильев Иван Сергеевич", salary=Decimal("45500.00"),
            enter_date=date(2022, 5, 17), phone_number="+79165555555",
            home_address="пр. Заводской, д.3"
        ),
        models.Worker(
            role_id=roles[0].id, pharmacy_id=pharmacies[2].id,
            FIO="Николаева Мария Дмитриевна", salary=Decimal("46500.00"),
            enter_date=date(2023, 1, 30), phone_number="+79166666666",
            home_address="ул. Школьная, д.9"
        ),
        models.Worker(
            role_id=roles[0].id, pharmacy_id=pharmacies[3].id,
            FIO="Алексеев Павел Олегович", salary=Decimal("44000.00"),
            enter_date=date(2021, 9, 12), phone_number="+79167777777",
            home_address="ул. Молодежная, д.11"
        ),
        models.Worker(
            role_id=roles[0].id, pharmacy_id=pharmacies[3].id,
            FIO="Федорова Екатерина Викторовна", salary=Decimal("49000.00"),
            enter_date=date(2022, 7, 8), phone_number="+79168888888",
            home_address="пр. Солнечный, д.4"
        ),
        models.Worker(
            role_id=roles[0].id, pharmacy_id=pharmacies[4].id,
            FIO="Дмитриев Андрей Николаевич", salary=Decimal("47500.00"),
            enter_date=date(2023, 3, 25), phone_number="+79169999999",
            home_address="ул. Речная, д.8"
        ),
        models.Worker(
            role_id=roles[0].id, pharmacy_id=pharmacies[4].id,
            FIO="Сергеева Татьяна Борисовна", salary=Decimal("48500.00"),
            enter_date=date(2022, 8, 14), phone_number="+79160000000",
            home_address="пр. Гагарина, д.15"
        ),
        
        models.Worker(
            role_id=roles[1].id, pharmacy_id=pharmacies[0].id,
            FIO="Козлов Александр Викторович", salary=Decimal("70000.00"),
            enter_date=date(2021, 5, 10), phone_number="+79151112233",
            home_address="ул. Парковая, д.20"
        ),
        models.Worker(
            role_id=roles[1].id, pharmacy_id=pharmacies[1].id,
            FIO="Орлова Виктория Сергеевна", salary=Decimal("72000.00"),
            enter_date=date(2022, 4, 18), phone_number="+79152223344",
            home_address="пр. Ленинградский, д.25"
        ),
        models.Worker(
            role_id=roles[1].id, pharmacy_id=pharmacies[2].id,
            FIO="Белов Станислав Иванович", salary=Decimal("71000.00"),
            enter_date=date(2020, 12, 3), phone_number="+79153334455",
            home_address="ул. Мира, д.30"
        ),
        models.Worker(
            role_id=roles[1].id, pharmacy_id=pharmacies[3].id,
            FIO="Григорьева Анастасия Петровна", salary=Decimal("73000.00"),
            enter_date=date(2023, 1, 15), phone_number="+79154445566",
            home_address="пр. Строителей, д.35"
        ),
        models.Worker(
            role_id=roles[1].id, pharmacy_id=pharmacies[4].id,
            FIO="Тимофеев Артем Дмитриевич", salary=Decimal("69000.00"),
            enter_date=date(2021, 8, 22), phone_number="+79155556677",
            home_address="ул. Зеленая, д.40"
        ),
        
        models.Worker(
            role_id=roles[2].id, pharmacy_id=pharmacies[0].id,
            FIO="Семенов Максим Андреевич", salary=Decimal("85000.00"),
            enter_date=date(2020, 7, 15), phone_number="+79156667788",
            home_address="пр. Победы, д.50"
        ),
        models.Worker(
            role_id=roles[3].id, pharmacy_id=pharmacies[0].id,
            FIO="Павлова Ольга Игоревна", salary=Decimal("87000.00"),
            enter_date=date(2021, 3, 12), phone_number="+79157778899",
            home_address="ул. Сосновая, д.55"
        )
    ]
    session.add_all(workers)
    session.commit()

    suppliers = [
        models.Supplier(
            name="ФармаГрупп", 
            additional_info="Официальный дистрибьютор",
            email="farmagroup@mail.ru", 
            phone_number="+78001234567"
        ),
        models.Supplier(
            name="МедТехСнаб", 
            additional_info="Оптовые поставки",
            email="medteh@snab.com", 
            phone_number="+78009876543"
        ),
        models.Supplier(
            name="Аптечный Альянс", 
            additional_info="Региональный поставщик",
            email="aptalliance@biz.ru", 
            phone_number="+78005556677"
        )
    ]
    session.add_all(suppliers)
    session.commit()


    availible_medicines = [

        models.AvailibleMedicineList(supplier_id=suppliers[0].id, medicine_id=medicines[0].id),
        models.AvailibleMedicineList(supplier_id=suppliers[0].id, medicine_id=medicines[1].id),
        models.AvailibleMedicineList(supplier_id=suppliers[0].id, medicine_id=medicines[2].id),
        models.AvailibleMedicineList(supplier_id=suppliers[0].id, medicine_id=medicines[3].id),
        models.AvailibleMedicineList(supplier_id=suppliers[0].id, medicine_id=medicines[6].id),
        

        models.AvailibleMedicineList(supplier_id=suppliers[1].id, medicine_id=medicines[4].id),
        models.AvailibleMedicineList(supplier_id=suppliers[1].id, medicine_id=medicines[5].id),
        models.AvailibleMedicineList(supplier_id=suppliers[1].id, medicine_id=medicines[7].id),
        models.AvailibleMedicineList(supplier_id=suppliers[1].id, medicine_id=medicines[8].id),
        models.AvailibleMedicineList(supplier_id=suppliers[1].id, medicine_id=medicines[9].id),
        
 
        models.AvailibleMedicineList(supplier_id=suppliers[2].id, medicine_id=medicines[10].id),
        models.AvailibleMedicineList(supplier_id=suppliers[2].id, medicine_id=medicines[11].id),
        models.AvailibleMedicineList(supplier_id=suppliers[2].id, medicine_id=medicines[12].id),
        models.AvailibleMedicineList(supplier_id=suppliers[2].id, medicine_id=medicines[13].id),
        models.AvailibleMedicineList(supplier_id=suppliers[2].id, medicine_id=medicines[14].id),
    ]
    session.add_all(availible_medicines)
    session.commit()

    doctors = [
        models.Doctor(name="Смирнов Александр Иванович", license_number=12345),
        models.Doctor(name="Ковалева Мария Сергеевна", license_number=23456),
        models.Doctor(name="Петров Игорь Васильевич", license_number=34567),
        models.Doctor(name="Никитина Ольга Дмитриевна", license_number=45678),
        models.Doctor(name="Фролов Денис Андреевич", license_number=56789)
    ]
    session.add_all(doctors)
    session.commit()

    clients = [
        models.Client(name="Иванов Алексей"),
        models.Client(name="Сидорова Екатерина"),
        models.Client(name="Петрова Анна"),
        models.Client(name="Козлов Михаил"),
        models.Client(name="Васильева Ольга"),
        models.Client(name="Николаев Денис"),
        models.Client(name="Макарова Виктория"),
        models.Client(name="Андреев Павел"),
        models.Client(name="Григорьева Ирина"),
        models.Client(name="Тимофеев Артем"),
        models.Client(name="Орлова Наталья"),
        models.Client(name="Белов Сергей"),
        models.Client(name="Кузьмина Татьяна"),
        models.Client(name="Дмитриев Андрей"),
        models.Client(name="Соколова Елена"),
        models.Client(name="Федоров Максим"),
        models.Client(name="Жукова Анастасия"),
        models.Client(name="Лебедев Иван"),
        models.Client(name="Волкова Светлана"),
        models.Client(name="Семенов Дмитрий")
    ]
    session.add_all(clients)
    session.commit()

    recipes = [
        models.Recipe(
            doctor_id=doctors[0].id, 
            client_id=clients[2].id, 
            medicine_id=medicines[3].id, 
            issue_date=date(2023, 5, 10)
        ),
        models.Recipe(
            doctor_id=doctors[1].id, 
            client_id=clients[5].id, 
            medicine_id=medicines[4].id,  
            issue_date=date(2023, 6, 15)
        ),
        models.Recipe(
            doctor_id=doctors[2].id, 
            client_id=clients[8].id, 
            medicine_id=medicines[5].id, 
            issue_date=date(2023, 4, 20)
        ),
        models.Recipe(
            doctor_id=doctors[3].id, 
            client_id=clients[12].id, 
            medicine_id=medicines[6].id, 
            issue_date=date(2023, 7, 1)
        ),
        models.Recipe(
            doctor_id=doctors[4].id, 
            client_id=clients[3].id, 
            medicine_id=medicines[3].id,  
            issue_date=date(2023, 5, 25)
        ),
        models.Recipe(
            doctor_id=doctors[0].id, 
            client_id=clients[7].id, 
            medicine_id=medicines[4].id,  
            issue_date=date(2023, 6, 5)
        ),
        models.Recipe(
            doctor_id=doctors[1].id, 
            client_id=clients[15].id, 
            medicine_id=medicines[5].id,  
            issue_date=date(2023, 7, 10)
        ),
        models.Recipe(
            doctor_id=doctors[2].id, 
            client_id=clients[18].id, 
            medicine_id=medicines[6].id,  
            issue_date=date(2023, 4, 15)
        )
    ]
    session.add_all(recipes)
    session.commit()

    type_pays = [
        models.TypePay(name="Наличные", additional_info="Оплата наличными в кассе"),
        models.TypePay(name="Карта", additional_info="Безналичная оплата картой"),
        models.TypePay(name="СБП", additional_info="Система быстрых платежей")
    ]
    session.add_all(type_pays)
    session.commit()


    shipments = [
        models.Shipment(
            supplier_id=suppliers[0].id, 
            date=date(2023, 1, 10), 
            comment="Первая поставка года", 
            invoice="INV-20230110-001"
        ),
        models.Shipment(
            supplier_id=suppliers[1].id, 
            date=date(2023, 2, 15), 
            comment="Февральская поставка", 
            invoice="INV-20230215-002"
        ),
        models.Shipment(
            supplier_id=suppliers[2].id, 
            date=date(2023, 3, 20), 
            comment="Весенняя поставка", 
            invoice="INV-20230320-003"
        ),
        models.Shipment(
            supplier_id=suppliers[0].id, 
            date=date(2023, 4, 5), 
            comment="Апрельский заказ", 
            invoice="INV-20230405-004"
        )
    ]
    session.add_all(shipments)
    session.commit()

    shipment_items = [
        models.ShipmentItems(
            shipment_id=shipments[0].id, 
            medicine_id=medicines[0].id, 
            count=500, 
            best_before_date=date(2024, 6, 1)
        ),
        models.ShipmentItems(
            shipment_id=shipments[0].id, 
            medicine_id=medicines[1].id, 
            count=400, 
            best_before_date=date(2024, 7, 15)
        ),
        models.ShipmentItems(
            shipment_id=shipments[0].id, 
            medicine_id=medicines[3].id, 
            count=200, 
            best_before_date=date(2024, 5, 20)
        ),
        
        models.ShipmentItems(
            shipment_id=shipments[1].id, 
            medicine_id=medicines[4].id, 
            count=150, 
            best_before_date=date(2024, 8, 10)
        ),
        models.ShipmentItems(
            shipment_id=shipments[1].id, 
            medicine_id=medicines[5].id, 
            count=250, 
            best_before_date=date(2024, 9, 5)
        ),
        models.ShipmentItems(
            shipment_id=shipments[1].id, 
            medicine_id=medicines[7].id, 
            count=300, 
            best_before_date=date(2024, 10, 15)
        ),
        
        models.ShipmentItems(
            shipment_id=shipments[2].id, 
            medicine_id=medicines[10].id, 
            count=350, 
            best_before_date=date(2024, 11, 20)
        ),
        models.ShipmentItems(
            shipment_id=shipments[2].id, 
            medicine_id=medicines[12].id, 
            count=450, 
            best_before_date=date(2024, 12, 1)
        ),
        
        models.ShipmentItems(
            shipment_id=shipments[3].id, 
            medicine_id=medicines[2].id, 
            count=200, 
            best_before_date=date(2024, 6, 15)
        ),
        models.ShipmentItems(
            shipment_id=shipments[3].id, 
            medicine_id=medicines[6].id, 
            count=100, 
            best_before_date=date(2024, 5, 30)
        )
    ]
    session.add_all(shipment_items)
    session.commit()

    warehouse_items = [
        models.WareHouse(
            shipment_item_id=item.id, 
            count=item.count  
        ) for item in shipment_items
    ]
    session.add_all(warehouse_items)
    session.commit()

    deliveries = [
        models.Delivery(date=date(2023, 1, 12)),
        models.Delivery(date=date(2023, 2, 18)),
        models.Delivery(date=date(2023, 3, 22)),
        models.Delivery(date=date(2023, 4, 7))
    ]
    session.add_all(deliveries)
    session.commit()

    stocks = []
    delivery_items = []
    
    for idx, item in enumerate(shipment_items):
        for ph_id in pharmacies[idx % len(pharmacies)].id, pharmacies[(idx+1) % len(pharmacies)].id:
            quantity = item.count // 3
            if quantity < 10: 
                quantity = item.count  
                
            stock = models.Stock(
                shipment_item_id=item.id,
                pharmacy_id=ph_id,
                count=quantity
            )
            session.add(stock)
            session.commit()
            
            delivery_items.append(
                models.DeliveryItems(
                    delivery_id=deliveries[idx % len(deliveries)].id,
                    stock_id=stock.id,
                    quantity=quantity
                )
            )
            
            wh_item = session.query(models.WareHouse).filter_by(
                shipment_item_id=item.id
            ).first()
            wh_item.count -= quantity

    session.add_all(delivery_items)
    session.commit()

    orders = []
    order_items = []
    
    pharmacists = workers[:10]
    
    for i in range(25):
        pharmacist = pharmacists[i % len(pharmacists)]
        client = clients[i % len(clients)]
        pay_type = type_pays[i % len(type_pays)]
        order_date = date(2023, 5, 1) + timedelta(days=i)
        
        order = models.Order(
            type_pay_id=pay_type.id,
            pharmacist_id=pharmacist.id,
            total_price=Decimal("0"), 
            date=order_date
        )
        session.add(order)
        session.flush() 
        
        total_price = Decimal("0")
        items_count = (i % 3) + 1
        
        for j in range(items_count):
            pharmacy_stocks = session.query(models.Stock).filter_by(
                pharmacy_id=pharmacist.pharmacy_id
            ).all()
            
            if not pharmacy_stocks:
                continue
                
            stock = pharmacy_stocks[j % len(pharmacy_stocks)]
            medicine = session.query(models.Medicine).get(stock.shipment_item.medicine_id)
            
            count = (i + j) % 3 + 1
            if count > stock.count:
                count = stock.count
                
            stock.count -= count
            
            recipe_id = None
            if medicine.need_recipe:
                recipe = session.query(models.Recipe).filter_by(
                    medicine_id=medicine.id,
                    client_id=client.id
                ).first()
                if recipe:
                    recipe_id = recipe.id
            
            order_item = models.OrderItems(
                order_id=order.id,
                medicine_id=medicine.id,
                stock_id=stock.id,
                count=count,
                recipe_id=recipe_id
            )
            order_items.append(order_item)
            
            total_price += medicine.price * count
        
        order.total_price = total_price
    
    session.add_all(order_items)
    session.commit()

    print("✅ Тестовые данные успешно заполнены!")