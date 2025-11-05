# utils/mediapipe_helper.py
import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None  # ← Will be updated

    def process_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)  # ← SAVE RESULTS
        return frame

    def draw_landmarks(self, frame):
        if self.results and self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def get_landmarks(self):
        if self.results and self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            return np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
        return None