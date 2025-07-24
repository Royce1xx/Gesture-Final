import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gesture Controller - Home")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #0d1117; color: white;")

        layout = QVBoxLayout()
        layout.setSpacing(20)

        # --- Top Bar ---
        top_bar = QHBoxLayout()
        top_bar.addWidget(QPushButton("🏠"))
        top_bar.addStretch()

        logo = QLabel("LOGO")
        logo.setFont(QFont("Segoe UI", 18, QFont.Bold))
        logo.setAlignment(Qt.AlignCenter)
        top_bar.addWidget(logo)
        top_bar.addStretch()

        top_bar.addWidget(QPushButton("⚙"))
        top_bar.addWidget(QPushButton("❓"))
        layout.addLayout(top_bar)

        # --- Welcome + Premium Offer ---
        welcome = QLabel("Welcome back, User 👋")
        welcome.setFont(QFont("Segoe UI", 16))
        layout.addWidget(welcome)

        premium = QPushButton("✨ Unlock Premium Features")
        premium.setStyleSheet("background-color: #80dfff; color: black; padding: 10px; border-radius: 8px;")
        layout.addWidget(premium)

        # --- Current Gesture ---
        gesture_display = QLabel("🖐️ Current Gesture: Fist")
        gesture_display.setFont(QFont("Segoe UI", 14))
        gesture_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(gesture_display)

        # --- Control Buttons ---
        control_buttons = QHBoxLayout()
        train = QPushButton("🧪 Train New Gesture")
        screen = QPushButton("📸 Screenshot")

        for btn in [train, screen]:
            btn.setStyleSheet("background-color: #1b1f27; padding: 12px; border-radius: 8px;")

        control_buttons.addWidget(train)
        control_buttons.addWidget(screen)
        layout.addLayout(control_buttons)

        # --- Feedback + Donations ---
        support_row = QHBoxLayout()
        support_row.addWidget(QPushButton("Feedback"))
        support_row.addWidget(QPushButton("💖 Donations"))
        layout.addLayout(support_row)

        # --- Disable Gesture Control ---
        bottom = QHBoxLayout()
        bottom.addStretch()
        disable = QPushButton("🔴 Disable Gesture Control")
        disable.setStyleSheet("background-color: #a00; padding: 10px; color: white; border-radius: 8px;")
        bottom.addWidget(disable)
        layout.addLayout(bottom)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
