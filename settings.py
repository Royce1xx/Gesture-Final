import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QSlider, QSpinBox, QComboBox, QFrame
)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QPen
from PyQt5.QtCore import Qt, QTimer


class CalibrationPreview(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #0e1016; border-radius: 200px;")
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor("#80dfff"))
        pen.setWidth(8)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(10, 10, -10, -10)
        angle_span = int(360 * self.progress / 100)
        painter.drawArc(rect, -90 * 16, angle_span * 16)

    def start_calibration(self):
        self.progress = 0
        self.timer.start(100)

    def update_progress(self):
        if self.progress < 100:
            self.progress += 2
            self.update()
        else:
            self.timer.stop()


class HandCalibrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gesture Controller - Hand Calibration")
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("background-color: #0d1117; color: white;")

        main_layout = QHBoxLayout()

        # 🔹 Left Side: Camera + Calibration
        left_panel = QVBoxLayout()
        title = QLabel("🖐️ Set Up Your Hand ID")
        title.setFont(QFont("Segoe UI", 20))
        title.setAlignment(Qt.AlignCenter)

        instruction = QLabel("Move your hand slowly in a circular motion to complete calibration.")
        instruction.setWordWrap(True)
        instruction.setAlignment(Qt.AlignCenter)
        instruction.setStyleSheet("color: #b0b0b0;")

        self.preview = CalibrationPreview()

        self.calibrate_btn = QPushButton("Start Calibration")
        self.calibrate_btn.clicked.connect(self.preview.start_calibration)
        self.calibrate_btn.setStyleSheet("""
            QPushButton {
                background-color: #80dfff;
                color: black;
                font-weight: bold;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #a5e8ff;
            }
        """)

        left_panel.addWidget(title)
        left_panel.addSpacing(10)
        left_panel.addWidget(instruction)
        left_panel.addSpacing(10)
        left_panel.addWidget(self.preview, alignment=Qt.AlignCenter)
        left_panel.addSpacing(10)
        left_panel.addWidget(self.calibrate_btn, alignment=Qt.AlignCenter)
        left_panel.addStretch()

        # 🔸 Right Side: Settings Panel
        right_panel = QVBoxLayout()
        config_title = QLabel("Gesture Settings")
        config_title.setFont(QFont("Segoe UI", 18))
        config_title.setAlignment(Qt.AlignCenter)

        # Sensitivity
        sensitivity_label = QLabel("Sensitivity")
        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setMinimum(1)
        self.sensitivity_slider.setMaximum(100)
        self.sensitivity_slider.setValue(50)

        # Cooldown
        cooldown_label = QLabel("Cooldown (sec)")
        self.cooldown_input = QSpinBox()
        self.cooldown_input.setRange(0, 10)
        self.cooldown_input.setValue(1)

        # Confidence
        confidence_label = QLabel("Confidence Threshold")
        self.confidence_slider = QSlider(Qt.Horizontal)
        self.confidence_slider.setMinimum(50)
        self.confidence_slider.setMaximum(100)
        self.confidence_slider.setValue(85)

        # Model Type
        model_label = QLabel("Detection Model")
        self.model_dropdown = QComboBox()
        self.model_dropdown.addItems(["Fast", "Accurate"])

        # Save Button
        save_btn = QPushButton("Save & Apply")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #80dfff;
                color: black;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #a5e8ff;
            }
        """)

        # Add to right panel
        right_panel.addWidget(config_title)
        right_panel.addSpacing(20)
        for widget in [
            sensitivity_label, self.sensitivity_slider,
            cooldown_label, self.cooldown_input,
            confidence_label, self.confidence_slider,
            model_label, self.model_dropdown,
            save_btn
        ]:
            right_panel.addWidget(widget)

        right_panel.addStretch()

        # Combine both panels
        main_layout.addLayout(left_panel, 2)
        main_layout.addLayout(right_panel, 1)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HandCalibrationWindow()
    window.show()
    sys.exit(app.exec_())
