# services/predictor.py
import os
import joblib
import numpy as np

MODEL_PATH = "data/model.pkl"

class GesturePredictor:
    def __init__(self):
        self.model = None
        self._load()

    def _load(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)

    def predict(self, landmarks):
        if self.model is None or landmarks is None:
            return "NO MODEL"
        arr = np.array(landmarks).reshape(1, -1)
        return self.model.predict(arr)[0].upper()