from utils.database import engine, Base
from model.db_model import GestureData

def initialize_database():
    """
    Ensure the database and tables are created.
    Call this once at startup.
    """
    print("🔧 Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created (if not already present).")
