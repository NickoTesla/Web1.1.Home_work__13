from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:567234@195.201.150.230:5433/lysiuk_fastapi" it was before, 
# below is a new row
SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# class Base(DeclarativeBase):
#     pass 

# lysiuk_fastapi name of database

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()