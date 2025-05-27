from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


DB_CONFIG = {
    'HOST': os.getenv('DB_HOST'),  
    'USER': os.getenv('DB_USER'),       
    'PASSWORD': os.getenv('DB_PASSWORD'),   
    'DATABASE': os.getenv('DB_DATABASE'),
    'PORT': os.getenv('DB_PORT', '3306'),      
    'CHARSET': os.getenv('DB_CHARSET', 'utf8mb4')
}


DATABASE_URL = (
    f"mysql+pymysql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}"
    f"@{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}"
    f"/{DB_CONFIG['DATABASE']}?charset={DB_CONFIG['CHARSET']}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, 
    pool_recycle=3600,  
    echo=False          
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()