import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QFrame, QSizePolicy, QStackedWidget
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from settings import HandCalibrationWindow

class SlimCard(QFrame):
    def __init__(self, title, subtitle="", icon="", parent=None):
        super().__init__(parent)
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
        self.title_label.setWordWrap(True)
        self.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        text_layout.addWidget(self.title_label)

        if subtitle:
            self.subtitle_label = QLabel(subtitle)
            self.subtitle_label.setFont(QFont("Segoe UI", 11))
            self.subtitle_label.setWordWrap(True)
            self.subtitle_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            text_layout.addWidget(self.subtitle_label)

        layout.addLayout(text_layout)

        self.arrow = QLabel("→")
        self.arrow.setFont(QFont("Segoe UI", 16))
        self.arrow.setFixedWidth(20)
        self.arrow.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.arrow)

        self.setLayout(layout)
        self.setup_glow()
        self.apply_theme(True)

    def apply_theme(self, is_dark):
        if is_dark:
            self.setStyleSheet("background-color: transparent;")
            self.title_label.setStyleSheet("color: #ffffff;")
            if hasattr(self, 'subtitle_label') and self.subtitle_label:
                self.subtitle_label.setStyleSheet("color: #aaaaaa;")
            self.arrow.setStyleSheet("color: #40e0ff;")
        else:
            self.setStyleSheet("background-color: transparent;")
            self.title_label.setStyleSheet("color: #1a237e;")
            if hasattr(self, 'subtitle_label') and self.subtitle_label:
                self.subtitle_label.setStyleSheet("color: #546e7a;")
            self.arrow.setStyleSheet("color: #1e88e5;")

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
        self.stacked_widget = QStackedWidget()
        self.main_widget = QWidget()
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.setWindowTitle("Gesture Controller")
        self.resize(950, 650)

        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(25)
        self.main_layout.setContentsMargins(30, 30, 30, 30)

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
        self.theme_btn.setStyleSheet("color: #ffffff; background-color: #222; border: 1px solid #444; border-radius: 20px;")
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
        self.status_dot = QLabel("●")
        self.status_dot.setFont(QFont("Segoe UI", 10))
        self.status_text = QLabel("Fist")
        self.status_text.setFont(QFont("Segoe UI", 16, QFont.Medium))
        self.status_text.setAlignment(Qt.AlignCenter)

        status_layout.addWidget(self.status_dot)
        status_layout.addWidget(self.status_text)

        gesture_section.addWidget(self.gesture_header)
        gesture_section.addLayout(status_layout)
        header_layout.addLayout(gesture_section)

        self.main_layout.addLayout(header_layout)

        self.welcome = QLabel("Welcome back, Royce")
        self.welcome.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.welcome.setAlignment(Qt.AlignCenter)
        self.welcome_glow = QGraphicsDropShadowEffect()
        self.welcome_glow.setBlurRadius(40)
        self.welcome_glow.setOffset(0, 0)
        self.welcome.setGraphicsEffect(self.welcome_glow)
        self.main_layout.addWidget(self.welcome)

        cards_layout = QVBoxLayout()
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

        self.main_layout.addLayout(cards_layout)

        self.stacked_widget.addWidget(self.main_widget)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.apply_theme()

    def go_back_home(self):
        self.stacked_widget.setCurrentWidget(self.main_widget)

    def apply_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet("background-color: #0d1b2a;")
            self.logo.setStyleSheet("color: #40e0ff;")
            self.theme_btn.setText("☀️")
            self.theme_btn.setStyleSheet("color: #ffffff; background-color: #222; border: 1px solid #444; border-radius: 20px;")
            self.status_dot.setStyleSheet("color: #00ff88;")
            self.status_text.setStyleSheet("color: white;")
            self.welcome.setStyleSheet("color: white;")
        else:
            self.setStyleSheet("background-color: #f8fbff;")
            self.logo.setStyleSheet("color: #1e88e5;")
            self.theme_btn.setText("🌙")
            self.theme_btn.setStyleSheet("color: #1a237e; background-color: #ddeeff; border: 1px solid #aaccff; border-radius: 20px;")
            self.status_dot.setStyleSheet("color: #00c853;")
            self.status_text.setStyleSheet("color: #1a237e;")
            self.welcome.setStyleSheet("color: #1a237e;")

        for card in self.cards:
            card.apply_theme(self.is_dark_theme)

    def open_settings(self, event):
        self.calibration_page = QWidget()
        layout = QVBoxLayout(self.calibration_page)

        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(100, 36)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #40e0ff;
                color: black;
                font-weight: bold;
                font-size: 13px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #66ebff;
            }
        """)
        back_btn.clicked.connect(self.go_back_home)
        layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        calibration_widget = HandCalibrationWindow()
        layout.addWidget(calibration_widget)

        self.stacked_widget.addWidget(self.calibration_page)
        self.stacked_widget.setCurrentWidget(self.calibration_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
