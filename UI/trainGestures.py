import cv2
import json
import random
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QLineEdit, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap


class TrainGestureWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0d1117; color: white;")
        self.cap = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.current_frame = None

        # UI
        self.video_label = QLabel("📷 Camera not started")
        self.video_label.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter gesture name...")
        self.name_input.setStyleSheet("padding: 8px; font-size: 14px;")

        self.start_btn = QPushButton("▶ Start Camera")
        self.start_btn.setStyleSheet("background-color: #80dfff; padding: 10px; font-weight: bold;")
        self.start_btn.clicked.connect(self.start_camera)

        self.capture_btn = QPushButton("📸 Capture Gesture")
        self.capture_btn.setEnabled(False)
        self.capture_btn.setStyleSheet("background-color: #4a90e2; padding: 10px; font-weight: bold;")
        self.capture_btn.clicked.connect(self.capture_gesture)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.name_input)

        button_row = QHBoxLayout()
        button_row.addWidget(self.start_btn)
        button_row.addWidget(self.capture_btn)
        layout.addLayout(button_row)

        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)
        self.capture_btn.setEnabled(True)
        self.status_label.setText("Camera started.")

    def update_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
        if self.current_frame is None:
            self.status_label.setText("❌ Camera not ready.")
            return

        vector = [round(random.uniform(0, 1), 2) for _ in range(21)]

        try:
            with open("gesture_data.json", "r") as f:
                data = json.load(f)
        except:
            data = {}

        data[name] = vector

        with open("gesture_data.json", "w") as f:
            json.dump(data, f, indent=2)

        self.status_label.setText(f"✅ Gesture '{name}' saved!")

    def stop_camera(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        self.timer.stop()

    def closeEvent(self, event):
        self.stop_camera()
        event.accept()
