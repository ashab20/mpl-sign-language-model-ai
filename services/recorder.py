# services/recorder.py
import cv2
import threading
from utils.mediapipe_helper import HandTracker
from model.db_model import GestureDatabase
from PIL import Image, ImageTk

class GestureRecorder:
    def __init__(self, view, label: str):
        self.view   = view
        self.label  = label.strip().upper()
        self.tracker = HandTracker()
        self.db      = GestureDatabase()
        self.collected = 0
        self.target    = 100
        self.running   = False

    # ----------------------------------------------------------
    def start(self):
        if self.running:
            return
        self.running = True
        self.collected = 0
        self.view.update_status(f"Recording '{self.label}' … 0/{self.target}")
        threading.Thread(target=self._loop, daemon=True).start()

    # ----------------------------------------------------------
    def _loop(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.view.root.after(0,
                                   lambda: self.view.update_status("Camera failed!"))
            self.running = False
            return

        while self.running and self.collected < self.target:
            ret, frame = cap.read()
            if not ret:
                break

            # MediaPipe
            self.tracker.process_frame(frame)
            frame = self.tracker.draw_landmarks(frame)

            lm = self.tracker.get_landmarks()
            if lm is not None:
                self.db.add_gesture(self.label, lm.tolist())
                self.collected += 1
                self.view.root.after(0,
                    lambda c=self.collected: self.view.update_status(
                        f"Recording '{self.label}' … {c}/{self.target}"
                    ))

            # preview on canvas
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil = Image.fromarray(rgb).resize((480, 360))
            tk_img = ImageTk.PhotoImage(pil)
            self.view.root.after(0, lambda i=tk_img: self.view.draw_on_canvas(i))

        cap.release()
        self.running = False
        msg = (f"Finished! {self.collected} frames saved for '{self.label}'."
               if self.collected == self.target else "Recording stopped.")
        self.view.root.after(0, lambda: self.view.update_status(msg))
        self.db.close()