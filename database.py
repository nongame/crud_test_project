from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:13@localhost:5438/postgres"

engine = create_engine(DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

