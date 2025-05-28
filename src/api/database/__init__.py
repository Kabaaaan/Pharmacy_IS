from .fill_test_data import fill_database
from .session import engine, SessionLocal
from .models import Base

def init_db():
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)
        # fill_database(db)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()