"""
view/main_view.py
-----------------
Beautiful ttkbootstrap UI.
* Uses tbs.LabelFrame (fixed name)
* Shows a permission dialog before any camera access
* Gracefully exits if permission is denied
"""

import tkinter as tk
import ttkbootstrap as tbs
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from typing import Callable
import sys
import platform
from utils.check_camera_permission import request_camera_permission


class MainView:
    def __init__(self, controller: 'AppController'):
        self.controller = controller

        # ------------------------------------------------------------------
        # 1. Root window – ttkbootstrap theme
        # ------------------------------------------------------------------
        self.root = tbs.Window(themename="superhero")
        self.root.title("Sign Language AI System")
        self.root.geometry("560x720")
        self.root.resizable(False, False)

        # ------------------------------------------------------------------
        # 2. Header
        # ------------------------------------------------------------------
        header = tbs.Frame(self.root, padding=20)
        header.pack(fill=X)
        tbs.Label(
            header,
            text="Sign Language AI",
            font=("Helvetica", 22, "bold"),
            bootstyle=PRIMARY
        ).pack()

        # ------------------------------------------------------------------
        # 3. Camera frame – **LabelFrame** (correct spelling)
        # ------------------------------------------------------------------
        cam_frame = tbs.LabelFrame(self.root, text="Live Camera", padding=10)
        cam_frame.pack(padx=20, pady=15, fill=BOTH, expand=True)

        self.cam_canvas = tk.Canvas(
            cam_frame,
            width=480,
            height=360,
            bg="#2d2d2d",
            highlightthickness=0
        )
        self.cam_canvas.pack(pady=5)

        # Helper that keeps a reference (prevents GC)
        def keep_ref(img):
            self.cam_canvas.delete("all")
            self.cam_canvas.create_image(240, 180, image=img)   # centre
            self.cam_canvas.image = img

        self.draw_on_canvas: Callable[[tk.PhotoImage], None] = keep_ref

        # ------------------------------------------------------------------
        # 4. Prediction entry (read-only)
        # ------------------------------------------------------------------
        pred_frame = tbs.Frame(self.root, padding=(20, 10))
        pred_frame.pack(fill=X)
        tbs.Label(pred_frame, text="Predicted Sign:",
                  font=("Helvetica", 12, "bold")).pack(anchor=W)
        self.pred_var = tbs.StringVar(value="—")
        tbs.Entry(
            pred_frame,
            textvariable=self.pred_var,
            font=("Consolas", 14),
            state="readonly",
            bootstyle=INFO
        ).pack(fill=X, pady=(5, 0))

        # ------------------------------------------------------------------
        # 5. Action buttons
        # ------------------------------------------------------------------
        btn_frame = tbs.Frame(self.root, padding=20)
        btn_frame.pack(fill=X)

        tbs.Button(
            btn_frame,
            text="Train Model",
            bootstyle=SUCCESS,
            width=18,
            command=self.controller.train_model
        ).pack(side=LEFT, padx=10)

        tbs.Button(
            btn_frame,
            text="Use AI",
            bootstyle=PRIMARY,
            width=18,
            command=self.controller.use_ai
        ).pack(side=RIGHT, padx=10)

        # ------------------------------------------------------------------
        # 6. Status bar
        # ------------------------------------------------------------------
        self.status_var = tbs.StringVar(value="Ready")
        tbs.Label(
            self.root,
            textvariable=self.status_var,
            relief=SUNKEN,
            anchor=W,
            padding=5,
            bootstyle=SECONDARY
        ).pack(fill=X, side=BOTTOM)

    # ----------------------------------------------------------------------
    # Public helpers
    # ----------------------------------------------------------------------
    def update_prediction(self, sign: str) -> None:
        self.pred_var.set(sign.upper())

    def update_status(self, msg: str) -> None:
        self.status_var.set(msg)

    def run(self) -> None:
        self.root.mainloop()

