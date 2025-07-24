import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty


class SlimCard(QFrame):
    def __init__(self, title, subtitle="", icon=""):
        super().__init__()
        self.setFrameStyle(QFrame.NoFrame)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(60)  # Ensure minimum height
        
        layout = QHBoxLayout()
        layout.setContentsMargins(25, 18, 25, 18)
        layout.setSpacing(15)
        
        # Icon (if provided)
        if icon:
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Segoe UI", 18))
            icon_label.setFixedWidth(35)
            icon_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(icon_label)
        
        # Text content with better responsive handling
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 15, QFont.Medium))
        title_label.setStyleSheet("color: #ffffff;")
        title_label.setWordWrap(False)  # Prevent wrapping
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        text_layout.addWidget(title_label)
        
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setFont(QFont("Segoe UI", 11))
            subtitle_label.setStyleSheet("color: #888;")
            subtitle_label.setWordWrap(True)  # Allow subtitle to wrap if needed
            subtitle_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            text_layout.addWidget(subtitle_label)
        
        layout.addLayout(text_layout)
        
        # Arrow indicator - fixed width to prevent layout shifts
        arrow = QLabel("→")
        arrow.setFont(QFont("Segoe UI", 16))
        arrow.setStyleSheet("color: #40e0ff;")
        arrow.setFixedWidth(20)
        arrow.setAlignment(Qt.AlignCenter)
        layout.addWidget(arrow)
        
        self.setLayout(layout)
        self.setStyleSheet(self.card_style())
        self.setup_glow()
    
    def card_style(self):
        return """
        SlimCard {
            background: rgba(15, 20, 30, 0.6);
            border: 1px solid rgba(64, 224, 255, 0.15);
            border-radius: 8px;
        }
        SlimCard:hover {
            background: rgba(20, 30, 45, 0.8);
            border: 1px solid rgba(64, 224, 255, 0.3);
        }
        """
    
    def setup_glow(self):
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setColor(QColor(64, 224, 255, 40))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)
    
    def enterEvent(self, event):
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(35)
        glow.setColor(QColor(64, 224, 255, 80))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.setup_glow()
        super().leaveEvent(event)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Gesture Controller")
        self.setMinimumSize(950, 650)  # Increased minimum width to prevent text cutoff
        self.setStyleSheet("""
            HomePage {
                background: #030305;
                font-family: 'Segoe UI', system-ui;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(35)
        main_layout.setContentsMargins(50, 40, 50, 40)

        # Header with logo and status
        header_layout = QHBoxLayout()
        
        # Logo
        logo = QLabel("GESTURE")
        logo.setFont(QFont("Segoe UI", 28, QFont.Light))
        logo.setStyleSheet("""
            color: #40e0ff;
            letter-spacing: 4px;
        """)
        
        logo_glow = QGraphicsDropShadowEffect()
        logo_glow.setBlurRadius(30)
        logo_glow.setColor(QColor(64, 224, 255, 100))
        logo_glow.setOffset(0, 0)
        logo.setGraphicsEffect(logo_glow)
        
        header_layout.addWidget(logo)
        header_layout.addStretch()
        
        # Compact status indicator
        status_layout = QHBoxLayout()
        status_layout.setSpacing(8)
        
        status_dot = QLabel("●")
        status_dot.setFont(QFont("Segoe UI", 12))
        status_dot.setStyleSheet("color: #00ff88;")
        
        status_text = QLabel("Fist")
        status_text.setFont(QFont("Segoe UI", 14, QFont.Medium))
        status_text.setStyleSheet("color: #ccc;")
        
        status_layout.addWidget(status_dot)
        status_layout.addWidget(status_text)
        
        header_layout.addLayout(status_layout)
        
        main_layout.addLayout(header_layout)

        # Welcome message with more pop
        welcome = QLabel("Welcome back, Royce")
        welcome.setFont(QFont("Segoe UI", 32, QFont.Bold))
        welcome.setStyleSheet("""
            color: #ffffff;
            margin: 25px 0 35px 0;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(64, 224, 255, 0.1), 
                stop:1 rgba(64, 224, 255, 0.05));
            padding: 15px 0;
            border-radius: 8px;
        """)
        welcome.setAlignment(Qt.AlignCenter)
        
        # Add glow to welcome text
        welcome_glow = QGraphicsDropShadowEffect()
        welcome_glow.setBlurRadius(40)
        welcome_glow.setColor(QColor(64, 224, 255, 60))
        welcome_glow.setOffset(0, 0)
        welcome.setGraphicsEffect(welcome_glow)
        
        main_layout.addWidget(welcome)

        # Navigation cards
        cards_layout = QVBoxLayout()
        cards_layout.setSpacing(12)

        # Main navigation options
        nav_items = [
            ("Train New Gestures", "Create and customize gesture controls", "🎯"),
            ("Gesture Library", "Browse and manage saved gestures", "📚"),
            ("Live Recognition", "Real-time gesture testing and preview", "👁"),
            ("Settings & Config", "Adjust sensitivity and preferences", "⚙"),
            ("Analytics", "View usage stats and accuracy metrics", "📊")
        ]

        for title, subtitle, icon in nav_items:
            card = SlimCard(title, subtitle, icon)
            cards_layout.addWidget(card)

        main_layout.addLayout(cards_layout)
        
        # Add some bottom spacing
        main_layout.addStretch()

        # Quick actions at bottom
        quick_actions = QHBoxLayout()
        quick_actions.setSpacing(15)
        
        screenshot_btn = QPushButton("📸 Screenshot")
        screenshot_btn.setStyleSheet(self.quick_button_style())
        screenshot_btn.setCursor(Qt.PointingHandCursor)
        
        help_btn = QPushButton("❓ Help")
        help_btn.setStyleSheet(self.quick_button_style())
        help_btn.setCursor(Qt.PointingHandCursor)
        
        quick_actions.addStretch()
        quick_actions.addWidget(screenshot_btn)
        quick_actions.addWidget(help_btn)
        
        main_layout.addLayout(quick_actions)

        self.setLayout(main_layout)

    def quick_button_style(self):
        return """
        QPushButton {
            background: rgba(10, 15, 25, 0.7);
            color: #888;
            border: 1px solid rgba(64, 224, 255, 0.1);
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 13px;
        }
        QPushButton:hover {
            background: rgba(15, 25, 40, 0.8);
            color: #40e0ff;
            border: 1px solid rgba(64, 224, 255, 0.2);
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = HomePage()
    window.show()
    sys.exit(app.exec_())