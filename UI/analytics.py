from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0d1117; color: white;")

        layout = QVBoxLayout()

        title = QLabel("📊 Analytics")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Here's how your app is performing")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setStyleSheet("color: #bbbbbb;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(40)

        metrics = [
            ("Total Gestures Trained", "7"),
            ("Most Common Gesture", "Fist"),
            ("Total App Sessions", "12"),
            ("Avg. Detection Confidence", "93%")
        ]

        for label, value in metrics:
            row = QLabel(f"{label}:  <b style='color:#80dfff;'>{value}</b>")
            row.setFont(QFont("Segoe UI", 14))
            row.setAlignment(Qt.AlignCenter)
            layout.addWidget(row)

        self.setLayout(layout)
