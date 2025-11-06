
import json
from utils.database import Session
from model.gesture_data import GestureData

class GestureDatabase:
    def __init__(self):
        self.session = Session()

    def get_all_gestures(self):
        rows = self.session.query(GestureData.label, GestureData.data).all()
        return [(label, json.loads(data) if isinstance(data, str) else data) for label, data in rows]

    def add_gesture(self, label: str, data: list):
        g = GestureData(label=label.upper(), data=json.dumps(data))
        self.session.add(g)
        self.session.commit()

    def close(self):
        self.session.close()