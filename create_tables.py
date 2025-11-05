# create_tables.py
from utils.database import engine, Base
from model.gesture_data import GestureData

# Create all tables
Base.metadata.create_all(engine)

print("✅ Tables created successfully!")
