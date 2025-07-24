import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty


class GlowButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._glow_intensity = 20
        self.setup_glow()
    
    def setup_glow(self):
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(self._glow_intensity)
        self.glow_effect.setColor(QColor(64, 224, 255, 100))
        self.glow_effect.setOffset(0, 0)
        self.setGraphicsEffect(self.glow_effect)
    
    def enterEvent(self, event):
        self.glow_effect.setBlurRadius(35)
        self.glow_effect.setColor(QColor(64, 224, 255, 150))
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.glow_effect.setBlurRadius(20)
        self.glow_effect.setColor(QColor(64, 224, 255, 100))
        super().leaveEvent(event)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Gesture Controller")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("""
            HomePage {
                background: #050507;
                font-family: 'Segoe UI', system-ui;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(40)
        main_layout.setContentsMargins(60, 60, 60, 60)

        # Top spacing
        main_layout.addStretch(1)

        # Logo
        logo = QLabel("GESTURE")
        logo.setFont(QFont("Segoe UI", 42, QFont.Light))
        logo.setStyleSheet("""
            color: #40e0ff;
            letter-spacing: 8px;
            margin-bottom: 10px;
        """)
        logo.setAlignment(Qt.AlignCenter)
        
        # Logo glow
        logo_glow = QGraphicsDropShadowEffect()
        logo_glow.setBlurRadius(50)
        logo_glow.setColor(QColor(64, 224, 255, 120))
        logo_glow.setOffset(0, 0)
        logo.setGraphicsEffect(logo_glow)
        
        main_layout.addWidget(logo)

        # Current gesture display
        gesture_container = QFrame()
        gesture_container.setFixedSize(400, 200)
        gesture_layout = QVBoxLayout(gesture_container)
        gesture_layout.setContentsMargins(0, 0, 0, 0)
        gesture_layout.setSpacing(15)

        gesture_icon = QLabel("✊")
        gesture_icon.setFont(QFont("Segoe UI", 64))
        gesture_icon.setAlignment(Qt.AlignCenter)
        gesture_icon.setStyleSheet("color: #ffffff;")

        gesture_label = QLabel("Fist Detected")
        gesture_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        gesture_label.setAlignment(Qt.AlignCenter)
        gesture_label.setStyleSheet("color: #40e0ff;")

        gesture_layout.addWidget(gesture_icon)
        gesture_layout.addWidget(gesture_label)

        # Container styling with heavy glow
        gesture_container.setStyleSheet("""
            QFrame {
                background: rgba(10, 15, 20, 0.8);
                border: 1px solid rgba(64, 224, 255, 0.3);
                border-radius: 20px;
            }
        """)
        
        # Main gesture glow effect
        gesture_glow = QGraphicsDropShadowEffect()
        gesture_glow.setBlurRadius(80)
        gesture_glow.setColor(QColor(64, 224, 255, 80))
        gesture_glow.setOffset(0, 0)
        gesture_container.setGraphicsEffect(gesture_glow)

        # Center the gesture container
        gesture_center_layout = QHBoxLayout()
        gesture_center_layout.addStretch()
        gesture_center_layout.addWidget(gesture_container)
        gesture_center_layout.addStretch()
        main_layout.addLayout(gesture_center_layout)

        main_layout.addStretch(1)

        # Action buttons - only the essential ones
        action_layout = QHBoxLayout()
        action_layout.setSpacing(30)

        train_btn = GlowButton("Train Gesture")
        train_btn.setFixedSize(180, 50)
        train_btn.setStyleSheet(self.primary_button_style())
        train_btn.setCursor(Qt.PointingHandCursor)

        settings_btn = GlowButton("Settings")
        settings_btn.setFixedSize(120, 50)
        settings_btn.setStyleSheet(self.secondary_button_style())
        settings_btn.setCursor(Qt.PointingHandCursor)

        action_layout.addStretch()
        action_layout.addWidget(train_btn)
        action_layout.addWidget(settings_btn)
        action_layout.addStretch()

        main_layout.addLayout(action_layout)

        # Bottom spacing
        main_layout.addStretch(1)

        # Status indicator
        status_layout = QHBoxLayout()
        status_dot = QLabel("●")
        status_dot.setFont(QFont("Segoe UI", 16))
        status_dot.setStyleSheet("color: #00ff88;")
        
        status_text = QLabel("Active")
        status_text.setFont(QFont("Segoe UI", 14))
        status_text.setStyleSheet("color: #666;")

        status_layout.addStretch()
        status_layout.addWidget(status_dot)
        status_layout.addWidget(status_text)
        status_layout.addStretch()

        main_layout.addLayout(status_layout)

        self.setLayout(main_layout)

    def primary_button_style(self):
        return """
        GlowButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(64, 224, 255, 0.8), 
                stop:1 rgba(32, 178, 255, 0.6));
            color: #000000;
            border: none;
            border-radius: 12px;
            font-weight: bold;
            font-size: 16px;
        }
        GlowButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(80, 240, 255, 0.9), 
                stop:1 rgba(48, 194, 255, 0.7));
        }
        GlowButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(48, 200, 255, 0.7), 
                stop:1 rgba(24, 160, 255, 0.5));
        }
        """

    def secondary_button_style(self):
        return """
        GlowButton {
            background: rgba(15, 20, 25, 0.8);
            color: #40e0ff;
            border: 1px solid rgba(64, 224, 255, 0.4);
            border-radius: 12px;
            font-weight: bold;
            font-size: 16px;
        }
        GlowButton:hover {
            background: rgba(20, 30, 40, 0.9);
            border: 1px solid rgba(64, 224, 255, 0.6);
        }
        GlowButton:pressed {
            background: rgba(10, 15, 20, 0.9);
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = HomePage()
    window.show()
    sys.exit(app.exec_())