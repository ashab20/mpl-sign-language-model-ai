# model/ml_model.py
import cv2
import threading
from PIL import Image, ImageTk
from utils.mediapipe_helper import HandTracker
from services.predictor import GesturePredictor

class GestureModel:
    def __init__(self):
        self.tracker = HandTracker()
        self.predictor = GesturePredictor()
        self.is_running = False
        self.view = None

    def set_view(self, view):
        self.view = view

    def predict_live(self):
        if not self.view or self.is_running:
            return
        self.is_running = True
        self.view.update_status("Starting AI prediction...")
        threading.Thread(target=self._capture_loop, daemon=True).start()

    def _capture_loop(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.view.root.after(0, lambda: self.view.update_status("Camera failed!"))
            return

        while self.is_running:
            ret, frame = cap.read()
            if not ret: break

            self.tracker.process_frame(frame)
            frame = self.tracker.draw_landmarks(frame)

            landmarks = self.tracker.get_landmarks()
            pred = self.predictor.predict(landmarks)

            self.view.root.after(0, lambda p=pred: self.view.update_prediction(p))

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb).resize((480, 360))
            tk_img = ImageTk.PhotoImage(pil_img)
            self.view.root.after(0, lambda img=tk_img: self.view.draw_on_canvas(img))

        cap.release()
        self.is_running = False
        self.view.root.after(0, lambda: self.view.update_status("Stopped."))