from .session import engine, SessionLocal
from fill_test_data import fill_database
from .models import Base

def init_db():
    # Для пересоздания БД при запуске раскомментить строку ниже
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()