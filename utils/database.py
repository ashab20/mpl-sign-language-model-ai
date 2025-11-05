# utils/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

load_dotenv()

DB_USER     = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "3306")
DB_NAME     = os.getenv("DB_NAME", "sign_ai")


root_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
root_engine = create_engine(root_url, echo=False)
with root_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))
print(f"Database '{DB_NAME}' checked/created.")


DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Session = scoped_session(SessionLocal)
print("SQLAlchemy engine ready.")

Base = declarative_base()

# Import model to register it
from model.gesture_data import GestureData  # ← Critical!

# CREATE TABLE IF NOT EXISTS
Base.metadata.create_all(bind=engine)
print("Table 'gestures' created (if not exists).")