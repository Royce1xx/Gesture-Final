import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from settings import HandCalibrationWindow  # ✅ Import settings window

class SlimCard(QFrame):
    def __init__(self, title, subtitle="", icon="", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(60)

        layout = QHBoxLayout()
        layout.setContentsMargins(25, 18, 25, 18)
        layout.setSpacing(15)

        if icon:
            self.icon_label = QLabel(icon)
            self.icon_label.setFont(QFont("Segoe UI", 18))
            self.icon_label.setFixedWidth(35)
            self.icon_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)
        text_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 15, QFont.Medium))
        self.title_label.setWordWrap(False)
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        text_layout.addWidget(self.title_label)

        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setFont(QFont("Segoe UI", 11))
            self.subtitle_label.setWordWrap(True)
            self.subtitle_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            text_layout.addWidget(self.subtitle_label)
        else:
            self.subtitle_label = None

        layout.addLayout(text_layout)

        self.arrow = QLabel("→")
        self.arrow.setFont(QFont("Segoe UI", 16))
        self.arrow.setFixedWidth(20)
        self.arrow.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.arrow)

        self.setLayout(layout)
        self.setup_glow()

    def apply_theme(self, is_dark):
        if is_dark:
            self.setStyleSheet("""
                SlimCard {
                    background: rgba(15, 20, 30, 0.6);
                    border: 1px solid rgba(64, 224, 255, 0.15);
                    border-radius: 8px;
                }
                SlimCard:hover {
                    background: rgba(20, 30, 45, 0.8);
                    border: 1px solid rgba(64, 224, 255, 0.3);
                }
            """)
            self.title_label.setStyleSheet("color: #ffffff;")
            if self.subtitle_label:
                self.subtitle_label.setStyleSheet("color: #888;")
            self.arrow.setStyleSheet("color: #40e0ff;")
            self.glow.setColor(QColor(64, 224, 255, 40))
        else:
            self.setStyleSheet("""
                SlimCard {
                    background: rgba(255, 255, 255, 0.8);
                    border: 1px solid rgba(135, 206, 250, 0.3);
                    border-radius: 8px;
                }
                SlimCard:hover {
                    background: rgba(240, 248, 255, 0.9);
                    border: 1px solid rgba(135, 206, 250, 0.5);
                }
            """)
            self.title_label.setStyleSheet("color: #1a237e;")
            if self.subtitle_label:
                self.subtitle_label.setStyleSheet("color: #546e7a;")
            self.arrow.setStyleSheet("color: #1e88e5;")
            self.glow.setColor(QColor(135, 206, 250, 60))

    def setup_glow(self):
        self.glow = QGraphicsDropShadowEffect()
        self.glow.setBlurRadius(20)
        self.glow.setOffset(0, 0)
        self.setGraphicsEffect(self.glow)

    def enterEvent(self, event):
        self.glow.setBlurRadius(35)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.glow.setBlurRadius(20)
        super().leaveEvent(event)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True
        self.cards = []
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.setWindowTitle("Gesture Controller")
        self.setMinimumSize(950, 650)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(35)
        main_layout.setContentsMargins(50, 40, 50, 40)

        header_layout = QHBoxLayout()

        self.logo = QLabel("GESTURE")
        self.logo.setFont(QFont("Segoe UI", 28, QFont.Light))

        self.logo_glow = QGraphicsDropShadowEffect()
        self.logo_glow.setBlurRadius(30)
        self.logo_glow.setOffset(0, 0)
        self.logo.setGraphicsEffect(self.logo_glow)

        header_layout.addWidget(self.logo)

        self.theme_btn = QPushButton("☀️")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        header_layout.addStretch()

        gesture_section = QVBoxLayout()
        gesture_section.setSpacing(6)
        gesture_section.setAlignment(Qt.AlignCenter)

        self.gesture_header = QLabel("Current Hand Gesture")
        self.gesture_header.setFont(QFont("Segoe UI", 12))
        self.gesture_header.setAlignment(Qt.AlignCenter)

        status_layout = QHBoxLayout()
        status_layout.setSpacing(8)
        status_layout.setContentsMargins(0, 0, 0, 0)

        self.status_dot = QLabel("●")
        self.status_dot.setFont(QFont("Segoe UI", 10))
        self.status_text = QLabel("Fist")
        self.status_text.setFont(QFont("Segoe UI", 16, QFont.Medium))
        self.status_text.setAlignment(Qt.AlignCenter)

        status_layout.addWidget(self.status_dot)
        status_layout.addWidget(self.status_text)

        status_container = QHBoxLayout()
        status_container.addStretch()
        status_container.addLayout(status_layout)
        status_container.addStretch()

        gesture_section.addWidget(self.gesture_header)
        gesture_section.addLayout(status_container)

        header_layout.addLayout(gesture_section)
        main_layout.addLayout(header_layout)

        self.welcome = QLabel("Welcome back, Royce")
        self.welcome.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.welcome.setAlignment(Qt.AlignCenter)
        self.welcome_glow = QGraphicsDropShadowEffect()
        self.welcome_glow.setBlurRadius(40)
        self.welcome_glow.setOffset(0, 0)
        self.welcome.setGraphicsEffect(self.welcome_glow)
        main_layout.addWidget(self.welcome)

        cards_layout = QVBoxLayout()
        cards_layout.setSpacing(12)

        nav_items = [
            ("Train New Gestures", "Create and customize gesture controls", "🎯"),
            ("Gesture Library", "Browse and manage saved gestures", "📚"),
            ("Live Recognition", "Real-time gesture testing and preview", "👁"),
            ("Settings & Config", "Adjust sensitivity and preferences", "⚙"),
            ("Analytics", "View usage stats and accuracy metrics", "📊")
        ]

        for title, subtitle, icon in nav_items:
            card = SlimCard(title, subtitle, icon, self)
            self.cards.append(card)
            cards_layout.addWidget(card)

            if title == "Settings & Config":
                card.mousePressEvent = self.open_settings

        main_layout.addLayout(cards_layout)
        main_layout.addStretch()

        quick_actions = QHBoxLayout()
        quick_actions.setSpacing(15)

        self.screenshot_btn = QPushButton("📸 Screenshot")
        self.screenshot_btn.setCursor(Qt.PointingHandCursor)
        self.help_btn = QPushButton("❓ Help")
        self.help_btn.setCursor(Qt.PointingHandCursor)

        quick_actions.addStretch()
        quick_actions.addWidget(self.screenshot_btn)
        quick_actions.addWidget(self.help_btn)
        main_layout.addLayout(quick_actions)

        self.setLayout(main_layout)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def apply_theme(self):
        # Apply all your existing dark/light mode styling here
        ...
        for card in self.cards:
            card.apply_theme(self.is_dark_theme)

    # ✅ Opens settings.py calibration window
    def open_settings(self, event):
        self.settings_window = HandCalibrationWindow()
        self.settings_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
