# utils/camera_permission.py
import sys
import platform
import time
import cv2
from ttkbootstrap.dialogs import Messagebox


def _show_error_and_exit(title: str, message: str) -> None:
    Messagebox.show_error(title=title, message=message)
    sys.exit(1)


def request_camera_permission(parent=None) -> bool:
    """
    Uses ttkbootstrap Messagebox (safe on macOS).
    parent: main window root (required for modal dialog)
    """
    if platform.system() != "Darwin":
        return True

    while True:
        # Use default OK/Cancel buttons → no need to pass 'buttons'
        response = Messagebox.show_question(
            title="Camera Permission Required",
            message=(
                "This app needs access to your camera.\n\n"
                "Go to:\n"
                "System Settings → Privacy & Security → Camera\n"
                "→ Enable **Terminal** or your IDE.\n\n"
                "Then click **OK**."
            ),
            parent=parent  # ← Critical: modal to main window
        )

        if response == "Cancel":
            _show_error_and_exit("Permission Denied", "Camera access is required.")

        time.sleep(1.5)
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            return True
        cap.release()
        time.sleep(0.5)