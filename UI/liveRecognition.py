from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class LiveRecognitionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0d1117; color: white;")

        layout = QVBoxLayout()

        title = QLabel("👁 Live Gesture Recognition")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        desc = QLabel("This is where your gesture model will run in real-time.")
        desc.setFont(QFont("Segoe UI", 12))
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("color: #bbbbbb;")
        layout.addWidget(desc)

        self.status_label = QLabel("Current Gesture: ✋ None Detected")
        self.status_label.setFont(QFont("Segoe UI", 16))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("margin-top: 40px; color: #80dfff;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)