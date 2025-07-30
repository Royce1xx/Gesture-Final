# ✅ Updated trainGestures.py to show hand overlays in the GUI

import sys
import os
import cv2
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QLineEdit
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

from handtracker import HandTracker  # ✅ use custom model


class TrainGestureWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #0d1117; color: white;")

        self.cap = cv2.VideoCapture(0)
        self.hand_tracker = HandTracker()

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter gesture name...")
        self.name_input.setStyleSheet("padding: 8px; font-size: 14px;")

        self.capture_btn = QPushButton("📸 Capture Gesture")
        self.capture_btn.setStyleSheet("background-color: #80dfff; padding: 10px; font-weight: bold;")
        self.capture_btn.clicked.connect(self.capture_gesture)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.back_btn = QPushButton("← Back to Home")
        self.back_btn.setStyleSheet("background-color: #555; padding: 8px;")
        self.back_btn.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.capture_btn)
        layout.addWidget(self.status_label)
        layout.addWidget(self.back_btn)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            overlay_frame = frame.copy()
            _ = self.hand_tracker.extract_vector(overlay_frame)  # draw on overlay frame

            rgb = cv2.cvtColor(overlay_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pix = QPixmap.fromImage(image)
            self.video_label.setPixmap(pix)
            self.current_frame = frame

    def capture_gesture(self):
        name = self.name_input.text().strip().lower()

        if not name:
            self.status_label.setText("❌ Please enter a gesture name.")
            return

        if not hasattr(self, 'current_frame'):
            self.status_label.setText("❌ No frame available.")
            return

        vector = self.hand_tracker.extract_vector(self.current_frame)
        if not vector:
            self.status_label.setText("❌ No hand detected.")
            return

        try:
            with open("gesture_data.json", "r") as f:
                data = json.load(f)
        except:
            data = {}

        data[name] = vector

        with open("gesture_data.json", "w") as f:
            json.dump(data, f, indent=2)

        self.status_label.setText(f"✅ Gesture '{name}' saved!")

    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainGestureWindow()
    window.show()
    sys.exit(app.exec_())
