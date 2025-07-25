# settings.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QCheckBox, QSpinBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gesture Controller - Settings")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #0d1117; color: white;")

        layout = QVBoxLayout()

        # 🔘 Toggle Camera
        self.toggle_camera_checkbox = QCheckBox("Enable Camera")
        self.toggle_camera_checkbox.setChecked(True)
        layout.addWidget(self.toggle_camera_checkbox)

        # 🎚️ Sensitivity Slider
        sensitivity_label = QLabel("Gesture Sensitivity")
        self.sensitivity_slider = QSlider(Qt.Horizontal)
        self.sensitivity_slider.setMinimum(1)
        self.sensitivity_slider.setMaximum(100)
        self.sensitivity_slider.setValue(50)
        layout.addWidget(sensitivity_label)
        layout.addWidget(self.sensitivity_slider)

        # ⏱️ Cooldown Input
        cooldown_label = QLabel("Gesture Cooldown (seconds)")
        self.cooldown_input = QSpinBox()
        self.cooldown_input.setMinimum(0)
        self.cooldown_input.setMaximum(10)
        self.cooldown_input.setValue(1)
        layout.addWidget(cooldown_label)
        layout.addWidget(self.cooldown_input)

        # 💾 Save Button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #80dfff;
                padding: 10px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #a5e8ff;
            }
        """)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_settings(self):
        camera_enabled = self.toggle_camera_checkbox.isChecked()
        sensitivity = self.sensitivity_slider.value()
        cooldown = self.cooldown_input.value()

        print(f"Settings Saved:\n  Camera: {camera_enabled}\n  Sensitivity: {sensitivity}\n  Cooldown: {cooldown}")
        # 🔌 In the next step, we’ll persist this to a backend or file

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SettingsWindow()
    win.show()
    sys.exit(app.exec_())
