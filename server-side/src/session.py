from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()


# database configuration: 'postgresql://user:password@host:port/database_name'
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables")
else:
    print(DATABASE_URL)

# create database engine
engine = create_engine(DATABASE_URL, echo=True)  #echo=True logs the sql queries

# create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# dependency to get a database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

