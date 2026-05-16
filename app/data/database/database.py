import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, declarative_base

engine = db.create_engine("sqlite:///recipe.db", connect_args={"check_same_thread": False})
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()