from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class GestureLibraryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0d1117; color: white;")

        layout = QVBoxLayout()

        title = QLabel("📚 Gesture Library")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Browse saved gestures")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #aaaaaa; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("background-color: #1b1f27; padding: 10px; border-radius: 8px;")
        self.list_widget.addItem("✅ wave")
        self.list_widget.addItem("✅ fist")
        self.list_widget.addItem("✅ peace")
        layout.addWidget(self.list_widget)

        self.setLayout(layout)