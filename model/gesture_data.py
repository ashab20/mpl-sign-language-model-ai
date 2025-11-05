# model/gesture_data.py
from sqlalchemy import Column, Integer, String, JSON
from utils.database import Base

class GestureData(Base):
    __tablename__ = "gestures"  # ← Must match

    id    = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(50), nullable=False, index=True)
    data  = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<Gesture id={self.id} label={self.label}>"