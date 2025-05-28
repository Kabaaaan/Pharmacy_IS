from .session import engine, SessionLocal
from .models import Base

def init_db():

    # Base.metadata.drop_all(engine)
    # TODO: заполнение таблиц тестовыми данными. Формы - создание закупки, работа с сотрудниками, просмотр статистики работы аптеки.

    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()