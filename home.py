import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty


class SlimCard(QFrame):
    def __init__(self, title, subtitle="", icon="", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(60)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(25, 18, 25, 18)
        layout.setSpacing(15)
        
        # Icon (if provided)
        if icon:
            self.icon_label = QLabel(icon)
            self.icon_label.setFont(QFont("Segoe UI", 18))
            self.icon_label.setFixedWidth(35)
            self.icon_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.icon_label)
        
        # Text content
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
        
        # Arrow indicator
        self.arrow = QLabel("→")
        self.arrow.setFont(QFont("Segoe UI", 16))
        self.arrow.setFixedWidth(20)
        self.arrow.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.arrow)
        
        self.setLayout(layout)
        self.setup_glow()
    
    def apply_theme(self, is_dark):
        if is_dark:
            # Dark theme
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
            # Light theme
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
        # Color will be set by theme
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.glow.setBlurRadius(20)
        super().leaveEvent(event)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True  # Start with dark theme
        self.cards = []  # Store references to cards for theme updates
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.setWindowTitle("Gesture Controller")
        self.setMinimumSize(950, 650)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(35)
        main_layout.setContentsMargins(50, 40, 50, 40)

        # Header with logo, theme toggle, and current hand gesture
        header_layout = QHBoxLayout()
        
        # Logo
        self.logo = QLabel("GESTURE")
        self.logo.setFont(QFont("Segoe UI", 28, QFont.Light))
        
        self.logo_glow = QGraphicsDropShadowEffect()
        self.logo_glow.setBlurRadius(30)
        self.logo_glow.setOffset(0, 0)
        self.logo.setGraphicsEffect(self.logo_glow)
        
        header_layout.addWidget(self.logo)
        
        # Theme toggle button
        self.theme_btn = QPushButton("☀️")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.setCursor(Qt.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_btn)
        
        header_layout.addStretch()
        
        # Current Hand Gesture section - centered and stacked
        gesture_section = QVBoxLayout()
        gesture_section.setSpacing(6)
        gesture_section.setAlignment(Qt.AlignCenter)
        
        # Header text
        self.gesture_header = QLabel("Current Hand Gesture")
        self.gesture_header.setFont(QFont("Segoe UI", 12, QFont.Normal))
        self.gesture_header.setAlignment(Qt.AlignCenter)
        
        # Centered status indicator
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
        
        # Center the status layout
        status_container = QHBoxLayout()
        status_container.addStretch()
        status_container.addLayout(status_layout)
        status_container.addStretch()
        
        gesture_section.addWidget(self.gesture_header)
        gesture_section.addLayout(status_container)
        
        header_layout.addLayout(gesture_section)
        
        main_layout.addLayout(header_layout)

        # Welcome message
        self.welcome = QLabel("Welcome back, Royce")
        self.welcome.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.welcome.setAlignment(Qt.AlignCenter)
        
        self.welcome_glow = QGraphicsDropShadowEffect()
        self.welcome_glow.setBlurRadius(40)
        self.welcome_glow.setOffset(0, 0)
        self.welcome.setGraphicsEffect(self.welcome_glow)
        
        main_layout.addWidget(self.welcome)

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
            card = SlimCard(title, subtitle, icon, self)
            self.cards.append(card)
            cards_layout.addWidget(card)

        main_layout.addLayout(cards_layout)
        
        # Add some bottom spacing
        main_layout.addStretch()

        # Quick actions at bottom
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
        if self.is_dark_theme:
            # Dark theme
            self.theme_btn.setText("☀️")  # Sun icon for switching to light
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(64, 224, 255, 0.1);
                    border: 1px solid rgba(64, 224, 255, 0.3);
                    border-radius: 20px;
                    color: #40e0ff;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background: rgba(64, 224, 255, 0.2);
                }
            """)
            
            self.setStyleSheet("""
                HomePage {
                    background: #030305;
                    font-family: 'Segoe UI', system-ui;
                }
            """)
            
            self.logo.setStyleSheet("""
                color: #40e0ff;
                letter-spacing: 4px;
            """)
            self.logo_glow.setColor(QColor(64, 224, 255, 100))
            
            self.gesture_header.setStyleSheet("color: #ccc; background: transparent;")
            self.status_dot.setStyleSheet("color: #00ff88;")
            self.status_text.setStyleSheet("color: #fff; background: transparent;")
            
            self.welcome.setStyleSheet("""
                color: #ffffff;
                margin: 25px 0 35px 0;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(64, 224, 255, 0.1), 
                    stop:1 rgba(64, 224, 255, 0.05));
                padding: 15px 0;
                border-radius: 8px;
            """)
            self.welcome_glow.setColor(QColor(64, 224, 255, 60))
            
            self.screenshot_btn.setStyleSheet("""
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
            """)
            
            self.help_btn.setStyleSheet(self.screenshot_btn.styleSheet())
            
        else:
            # Light theme
            self.theme_btn.setText("🌙")  # Moon icon for switching to dark
            self.theme_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(135, 206, 250, 0.15);
                    border: 1px solid rgba(135, 206, 250, 0.4);
                    border-radius: 20px;
                    color: #1e88e5;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background: rgba(135, 206, 250, 0.25);
                }
            """)
            
            self.setStyleSheet("""
                HomePage {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #f8fbff, stop:0.3 #ffffff, 
                        stop:0.7 #f0f8ff, stop:1 #e6f3ff);
                    font-family: 'Segoe UI', system-ui;
                }
            """)
            
            self.logo.setStyleSheet("""
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e88e5, stop:0.5 #42a5f5, stop:1 #64b5f6);
                letter-spacing: 4px;
            """)
            self.logo_glow.setColor(QColor(30, 136, 229, 120))
            
            self.gesture_header.setStyleSheet("color: #7c8892; background: transparent;")
            self.status_dot.setStyleSheet("color: #00c853;")
            self.status_text.setStyleSheet("color: #1a237e; background: transparent;")
            
            self.welcome.setStyleSheet("""
                color: #1a237e;
                margin: 25px 0 35px 0;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(135, 206, 250, 0.12), 
                    stop:1 rgba(135, 206, 250, 0.06));
                padding: 15px 0;
                border-radius: 8px;
            """)
            self.welcome_glow.setColor(QColor(135, 206, 250, 80))
            
            self.screenshot_btn.setStyleSheet("""
                QPushButton {
                    background: rgba(135, 206, 250, 0.1);
                    color: #546e7a;
                    border: 1px solid rgba(135, 206, 250, 0.3);
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: rgba(135, 206, 250, 0.2);
                    color: #1e88e5;
                    border: 1px solid rgba(135, 206, 250, 0.5);
                }
            """)
            
            self.help_btn.setStyleSheet(self.screenshot_btn.styleSheet())
        
        # Apply theme to all cards
        for card in self.cards:
            card.apply_theme(self.is_dark_theme)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = HomePage()
    window.show()
    sys.exit(app.exec_())