
import tkinter as tk
import ttkbootstrap as tbs
from ttkbootstrap.constants import *
from typing import Callable
from utils.camera_permission import request_camera_permission


class MainView:
    """Main UI – all widgets, canvas, status bar, text input, animation controls."""

    def __init__(self, controller):
        self.controller = controller

        self.root = tbs.Window(themename="superhero")
        self.root.withdraw()                     # hide until permission granted
        self.root.title("Sign Language AI System")
        self.root.geometry("560x760")
        self.root.resizable(False, False)

        if not request_camera_permission(parent=self.root):
            self.root.destroy()
            return

        self._build_ui()
        self.root.deiconify()                    # now show the window

    def _build_ui(self):
        # ---------- Header ----------
        header = tbs.Frame(self.root, padding=10)
        header.pack(fill=X)
        tbs.Label(
            header,
            text="Sign Language AI",
            font=("Helvetica", 22, "bold"),
            bootstyle=PRIMARY,
        ).pack()

        # ---------- Live Camera ----------
        cam_frame = tbs.Labelframe(self.root, text="Live Camera", padding=10)
        cam_frame.pack(padx=10, pady=15, fill=BOTH, expand=True)

        self.cam_canvas = tk.Canvas(
            cam_frame,
            width=480,
            height=300,               # <-- you asked for 300 px height
            bg="#2d2d2d",
            highlightthickness=0,
        )
        self.cam_canvas.pack(pady=5)

        # keep a reference so the image isn’t garbage-collected
        def keep_ref(img: tk.PhotoImage):
            self.cam_canvas.delete("all")
            self.cam_canvas.create_image(240, 150, image=img, anchor="center")
            self.cam_canvas.image = img               # <-- critical!

        self.draw_on_canvas: Callable[[tk.PhotoImage], None] = keep_ref

        # ---------- Prediction ----------
        pred_frame = tbs.Frame(self.root, padding=(20, 10))
        pred_frame.pack(fill=X)

        tbs.Label(pred_frame, text="Predicted Sign:", font=("Helvetica", 12, "bold")).pack(anchor=W)
        self.pred_var = tbs.StringVar(value="—")
        tbs.Entry(
            pred_frame,
            textvariable=self.pred_var,
            font=("Consolas", 14),
            state="readonly",
            bootstyle=INFO,
        ).pack(fill=X, pady=(5, 0))

        # ---------- Record / Train / Use AI ----------
        btn_frame = tbs.Frame(self.root, padding=20)
        btn_frame.pack(fill=X)

        tbs.Button(
            btn_frame,
            text="Record Gesture",
            bootstyle=WARNING,
            width=18,
            command=self.controller.record_gesture,
        ).pack(side=LEFT, padx=10)

        tbs.Button(
            btn_frame,
            text="Train Model",
            bootstyle=SUCCESS,
            width=18,
            command=self.controller.train_model,
        ).pack(side=LEFT, padx=10)

        tbs.Button(
            btn_frame,
            text="Use AI",
            bootstyle=PRIMARY,
            width=18,
            command=self.controller.use_ai,
        ).pack(side=RIGHT, padx=10)

        # ---------- Text → Sign Animation ----------
        input_frame = tbs.Frame(self.root, padding=(20, 10))
        input_frame.pack(fill=X)

        self.text_var = tbs.StringVar(value="HELLO WORLD")
        tbs.Entry(
            input_frame,
            textvariable=self.text_var,
            font=("Consolas", 14),
        ).pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

        # Play Live / Record Video / Play Last
        tbs.Button(
            input_frame,
            text="Play Live",
            bootstyle=INFO,
            width=12,
            command=lambda: self.controller.play_text(record=False),
        ).pack(side=LEFT, padx=2)

        tbs.Button(
            input_frame,
            text="Record Video",
            bootstyle=DANGER,
            width=14,
            command=lambda: self.controller.play_text(record=True),
        ).pack(side=LEFT, padx=2)

        tbs.Button(
            input_frame,
            text="Play Last",
            bootstyle=SECONDARY,
            width=12,
            command=self.controller.play_last_video,
        ).pack(side=RIGHT, padx=2)

        # ---------- Status bar ----------
        self.status_var = tbs.StringVar(value="Ready")
        tbs.Label(
            self.root,
            textvariable=self.status_var,
            relief=SUNKEN,
            anchor=W,
            padding=5,
            bootstyle=SECONDARY,
        ).pack(fill=X, side=BOTTOM)

    def update_prediction(self, sign: str) -> None:
        self.pred_var.set(sign.upper())

    def update_status(self, msg: str) -> None:
        self.status_var.set(msg)

    def run(self) -> None:
        self.root.mainloop()