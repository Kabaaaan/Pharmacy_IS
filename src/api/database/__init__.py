from session import engine, SessionLocal
from models import Base

def init_db():
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()