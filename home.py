import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect, QFrame
)
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gesture Controller - Home")
        self.setMinimumSize(1000, 650)
        self.setStyleSheet("background-color: #0d1117;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # --- Glowing Top Navigation Bar ---
        top_bar = QHBoxLayout()
        top_bar.setSpacing(20)

        for icon in ["\U0001F3E0", "\U0001F504"]:
            btn = QPushButton(icon)
            btn.setToolTip("Home" if icon == "\U0001F3E0" else "Change Gesture")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(self.icon_button_style())
            top_bar.addWidget(btn)

        top_bar.addStretch()

        logo = QLabel("GESTURE ✋")
        logo.setFont(QFont("Segoe UI", 20, QFont.Bold))
        logo.setStyleSheet("color: #80dfff;")
        top_bar.addWidget(logo)

        top_bar.addStretch()

        for icon in ["\u2699", "\u2753"]:
            btn = QPushButton(icon)
            btn.setToolTip("Settings" if icon == "\u2699" else "Help")
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(self.icon_button_style())
            top_bar.addWidget(btn)

        main_layout.addLayout(top_bar)

        # --- Welcome Section ---
        welcome = QLabel("Welcome back, Royce 👋")
        welcome.setFont(QFont("Segoe UI", 22, QFont.Bold))
        welcome.setStyleSheet("color: white;")
        main_layout.addWidget(welcome)

        premium = QPushButton("✨ Unlock Premium Features")
        premium.setStyleSheet(self.primary_button_style())
        premium.setCursor(Qt.PointingHandCursor)
        main_layout.addWidget(premium)

        # --- Gesture Card ---
        gesture_card = QLabel("\n🖐️ Current Gesture:\nFist\n")
        gesture_card.setAlignment(Qt.AlignCenter)
        gesture_card.setFont(QFont("Segoe UI", 16))
        gesture_card.setStyleSheet("""
            background-color: #1b1f27;
            border-radius: 16px;
            color: white;
            padding: 30px;
        """)
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(50)
        glow.setColor(QColor("#80dfff"))
        glow.setOffset(0, 0)
        gesture_card.setGraphicsEffect(glow)
        main_layout.addWidget(gesture_card)

        # --- Action Buttons ---
        action_row = QHBoxLayout()
        for text in ["🧪 Train New Gesture", "📸 Screenshot"]:
            btn = QPushButton(text)
            btn.setStyleSheet(self.card_button_style())
            btn.setCursor(Qt.PointingHandCursor)
            action_row.addWidget(btn)
        main_layout.addLayout(action_row)

        # --- Support Row ---
        support_row = QHBoxLayout()
        for text in ["Feedback", "💖 Donations"]:
            btn = QPushButton(text)
            btn.setStyleSheet(self.outline_button_style())
            btn.setCursor(Qt.PointingHandCursor)
            support_row.addWidget(btn)
        main_layout.addLayout(support_row)

        # --- Disable Control ---
        disable = QPushButton("🔴 Disable Gesture Control")
        disable.setCursor(Qt.PointingHandCursor)
        disable.setStyleSheet("""
            QPushButton {
                background-color: #a00;
                color: white;
                padding: 12px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #c22;
            }
        """)
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        bottom_row.addWidget(disable)
        main_layout.addLayout(bottom_row)

        self.setLayout(main_layout)

    def icon_button_style(self):
        return """
        QPushButton {
            background-color: #1b1f27;
            border-radius: 20px;
            color: #80dfff;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: #263240;
        }
        """

    def primary_button_style(self):
        return """
        QPushButton {
            background-color: #80dfff;
            padding: 14px;
            color: black;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #a5e8ff;
        }
        """

    def card_button_style(self):
        return """
        QPushButton {
            background-color: #1b1f27;
            padding: 16px;
            font-size: 15px;
            color: white;
            border-radius: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #263240;
        }
        """

    def outline_button_style(self):
        return """
        QPushButton {
            padding: 10px;
            color: #80dfff;
            border: 2px solid #80dfff;
            border-radius: 10px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #11202c;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
