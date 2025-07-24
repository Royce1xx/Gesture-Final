import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QFrame, QSpacerItem, QSizePolicy, QGridLayout
)
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, pyqtProperty


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._glow_radius = 0
        self.animation = QPropertyAnimation(self, b"glow_radius")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
    
    @pyqtProperty(int)
    def glow_radius(self):
        return self._glow_radius
    
    @glow_radius.setter
    def glow_radius(self, radius):
        self._glow_radius = radius
        self.update()
    
    def enterEvent(self, event):
        self.animation.setStartValue(self._glow_radius)
        self.animation.setEndValue(20)
        self.animation.start()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.animation.setStartValue(self._glow_radius)
        self.animation.setEndValue(0)
        self.animation.start()
        super().leaveEvent(event)


class StatusCard(QFrame):
    def __init__(self, title, status, icon="🖐️"):
        super().__init__()
        self.setFrameStyle(QFrame.NoFrame)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(30, 25, 30, 25)
        
        # Icon and title row
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI", 24))
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet("color: #a0a9b8;")
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Status
        status_label = QLabel(status)
        status_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        status_label.setStyleSheet("color: #ffffff;")
        
        layout.addLayout(header_layout)
        layout.addWidget(status_label)
        
        self.setLayout(layout)
        self.setStyleSheet(self.card_style())
        
        # Add glow effect
        self.setup_glow_effect()
    
    def card_style(self):
        return """
        StatusCard {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #21262d, stop:1 #1c2128);
            border: 1px solid #30363d;
            border-radius: 16px;
        }
        """
    
    def setup_glow_effect(self):
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(25)
        glow.setColor(QColor(128, 223, 255, 60))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_animations()

    def setup_ui(self):
        self.setWindowTitle("Gesture Controller - Dashboard")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(self.main_styles())

        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 40, 50, 40)

        # Header
        main_layout.addLayout(self.create_header())
        
        # Welcome section
        main_layout.addLayout(self.create_welcome_section())
        
        # Status cards
        main_layout.addLayout(self.create_status_section())
        
        # Action buttons
        main_layout.addLayout(self.create_action_section())
        
        # Bottom section
        main_layout.addStretch()
        main_layout.addLayout(self.create_bottom_section())

        self.setLayout(main_layout)

    def main_styles(self):
        return """
        HomePage {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #0d1117, stop:0.3 #161b22, stop:1 #0d1117);
            font-family: 'Segoe UI', system-ui, sans-serif;
        }
        """

    def create_header(self):
        header_layout = QHBoxLayout()
        header_layout.setSpacing(25)

        # Left nav buttons
        nav_buttons = QHBoxLayout()
        nav_buttons.setSpacing(12)
        
        for icon, tooltip in [("🏠", "Home"), ("🔄", "Refresh"), ("⚙️", "Settings")]:
            btn = self.create_icon_button(icon, tooltip)
            nav_buttons.addWidget(btn)
        
        header_layout.addLayout(nav_buttons)
        header_layout.addStretch()

        # Logo
        logo = QLabel("GESTURE CONTROL")
        logo.setFont(QFont("Segoe UI Light", 32, QFont.Bold))
        logo.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #80dfff, stop:1 #4fc3f7);
            letter-spacing: 2px;
        """)
        logo.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo)

        header_layout.addStretch()

        # Right buttons
        right_buttons = QHBoxLayout()
        right_buttons.setSpacing(12)
        
        for icon, tooltip in [("❓", "Help"), ("📊", "Stats")]:
            btn = self.create_icon_button(icon, tooltip)
            right_buttons.addWidget(btn)
        
        header_layout.addLayout(right_buttons)
        
        return header_layout

    def create_welcome_section(self):
        welcome_layout = QVBoxLayout()
        welcome_layout.setSpacing(20)
        welcome_layout.setAlignment(Qt.AlignCenter)

        # Welcome text
        welcome = QLabel("Welcome back, Royce! 👋")
        welcome.setFont(QFont("Segoe UI", 36, QFont.Light))
        welcome.setStyleSheet("""
            color: #ffffff;
            padding: 10px;
        """)
        welcome.setAlignment(Qt.AlignCenter)

        # Subtitle
        subtitle = QLabel("Your gesture recognition system is active and ready")
        subtitle.setFont(QFont("Segoe UI", 16))
        subtitle.setStyleSheet("color: #8b949e; padding: 5px;")
        subtitle.setAlignment(Qt.AlignCenter)

        welcome_layout.addWidget(welcome)
        welcome_layout.addWidget(subtitle)

        return welcome_layout

    def create_status_section(self):
        status_layout = QHBoxLayout()
        status_layout.setSpacing(25)

        # Current gesture card
        gesture_card = StatusCard("Current Gesture", "Fist", "✊")
        
        # Accuracy card
        accuracy_card = StatusCard("Accuracy", "94.2%", "🎯")
        
        # Active time card
        time_card = StatusCard("Active Time", "2h 34m", "⏱️")

        status_layout.addWidget(gesture_card)
        status_layout.addWidget(accuracy_card)
        status_layout.addWidget(time_card)

        return status_layout

    def create_action_section(self):
        action_layout = QVBoxLayout()
        action_layout.setSpacing(20)

        # Premium button
        premium_btn = AnimatedButton("✨ Unlock Premium Features")
        premium_btn.setStyleSheet(self.premium_button_style())
        premium_btn.setFixedHeight(60)
        premium_btn.setCursor(Qt.PointingHandCursor)
        premium_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))

        # Action buttons grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        actions = [
            ("🧠 Train New Gesture", "Train a custom gesture for your needs"),
            ("📸 Take Screenshot", "Capture current gesture recognition"),
            ("📈 View Analytics", "Detailed performance metrics"),
            ("🎮 Gaming Mode", "Optimized for gaming controls")
        ]

        for i, (title, description) in enumerate(actions):
            btn = self.create_action_card(title, description)
            row, col = i // 2, i % 2
            grid_layout.addWidget(btn, row, col)

        action_layout.addWidget(premium_btn)
        action_layout.addLayout(grid_layout)

        return action_layout

    def create_bottom_section(self):
        bottom_layout = QVBoxLayout()
        bottom_layout.setSpacing(15)

        # Support buttons
        support_layout = QHBoxLayout()
        support_layout.setSpacing(15)
        
        feedback_btn = QPushButton("💬 Send Feedback")
        feedback_btn.setStyleSheet(self.outline_button_style())
        feedback_btn.setCursor(Qt.PointingHandCursor)
        
        donate_btn = QPushButton("❤️ Support Development")
        donate_btn.setStyleSheet(self.outline_button_style())
        donate_btn.setCursor(Qt.PointingHandCursor)

        support_layout.addWidget(feedback_btn)
        support_layout.addWidget(donate_btn)
        support_layout.addStretch()

        # Disable button
        disable_btn = QPushButton("🛑 Disable Gesture Recognition")
        disable_btn.setStyleSheet(self.danger_button_style())
        disable_btn.setCursor(Qt.PointingHandCursor)
        disable_btn.setFixedWidth(300)

        disable_layout = QHBoxLayout()
        disable_layout.addStretch()
        disable_layout.addWidget(disable_btn)

        bottom_layout.addLayout(support_layout)
        bottom_layout.addLayout(disable_layout)

        return bottom_layout

    def create_icon_button(self, icon, tooltip=""):
        btn = QPushButton(icon)
        btn.setFixedSize(50, 50)
        btn.setStyleSheet(self.icon_button_style())
        btn.setCursor(Qt.PointingHandCursor)
        btn.setToolTip(tooltip)
        btn.setFont(QFont("Segoe UI", 18))
        return btn

    def create_action_card(self, title, description):
        card = QFrame()
        card.setFrameStyle(QFrame.NoFrame)
        card.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Segoe UI", 12))
        desc_label.setStyleSheet("color: #8b949e;")
        desc_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        
        card.setLayout(layout)
        card.setStyleSheet(self.action_card_style())
        
        # Add subtle glow
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(15)
        glow.setColor(QColor(128, 223, 255, 30))
        glow.setOffset(0, 2)
        card.setGraphicsEffect(glow)
        
        return card

    def setup_animations(self):
        # Add any additional animations here
        pass

    # Style methods
    def icon_button_style(self):
        return """
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.08), 
                stop:1 rgba(255, 255, 255, 0.03));
            border: 1px solid rgba(128, 223, 255, 0.3);
            border-radius: 25px;
            color: #80dfff;
            font-weight: bold;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(128, 223, 255, 0.15), 
                stop:1 rgba(128, 223, 255, 0.08));
            border: 1px solid rgba(128, 223, 255, 0.5);
        }
        QPushButton:pressed {
            background: rgba(128, 223, 255, 0.2);
        }
        """

    def premium_button_style(self):
        return """
        AnimatedButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #80dfff, stop:0.5 #4fc3f7, stop:1 #29b6f6);
            color: #000000;
            border: none;
            border-radius: 15px;
            padding: 15px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        AnimatedButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #a6eeff, stop:0.5 #7dd3f0, stop:1 #4fc3f7);
            transform: translateY(-2px);
        }
        AnimatedButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #5dd5ff, stop:0.5 #29b6f6, stop:1 #0288d1);
        }
        """

    def action_card_style(self):
        return """
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #21262d, stop:1 #1c2128);
            border: 1px solid #30363d;
            border-radius: 12px;
        }
        QFrame:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #282e37, stop:1 #23272f);
            border: 1px solid #40464d;
        }
        """

    def outline_button_style(self):
        return """
        QPushButton {
            background: transparent;
            border: 2px solid #80dfff;
            color: #80dfff;
            border-radius: 10px;
            padding: 12px 20px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background: rgba(128, 223, 255, 0.1);
            border: 2px solid #a6eeff;
            color: #a6eeff;
        }
        QPushButton:pressed {
            background: rgba(128, 223, 255, 0.2);
        }
        """

    def danger_button_style(self):
        return """
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ff4757, stop:1 #ff3742);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 15px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ff6b7a, stop:1 #ff5252);
        }
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ff3d47, stop:1 #e53935);
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = HomePage()
    window.show()
    sys.exit(app.exec_())