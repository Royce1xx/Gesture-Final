from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

class SignUpWindow(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.switch_to_login = switch_to_login

        self.setWindowTitle("Gesture Controller - Sign Up")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #0d1117;")

        form_widget = QWidget()
        form_widget.setFixedWidth(380)
        form_widget.setStyleSheet("""
            background-color: #1b1f27;
            border-radius: 16px;
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(50)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(128, 223, 255))
        form_widget.setGraphicsEffect(shadow)

        self.glow_anim = QPropertyAnimation(shadow, b"blurRadius")
        self.glow_anim.setStartValue(40)
        self.glow_anim.setEndValue(70)
        self.glow_anim.setDuration(1500)
        self.glow_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.glow_anim.setLoopCount(-1)
        self.glow_anim.start()

        form_layout = QVBoxLayout()

        title = QLabel("Sign Up")
        title.setFont(QFont("Segoe UI", 26))
        title.setStyleSheet("color: #80dfff;")
        title.setAlignment(Qt.AlignCenter)

        email_input = QLineEdit()
        email_input.setPlaceholderText("Email")
        email_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background-color: #0e1016;
                border: 1px solid #80dfff;
                border-radius: 8px;
                color: white;
                font-size: 15px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                letter-spacing: 0.5px;
            }
        """)

        password_input = QLineEdit()
        password_input.setPlaceholderText("Password")
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setStyleSheet(email_input.styleSheet())

        signup_btn = QPushButton("Sign Up")
        signup_btn.setCursor(Qt.PointingHandCursor)
        signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #80dfff;
                padding: 12px;
                font-weight: bold;
                color: black;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #a5e8ff;
            }
        """)

        google_btn = QPushButton("Sign Up with Google")
        google_btn.setCursor(Qt.PointingHandCursor)
        google_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                padding: 12px;
                color: black;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e6e6e6;
            }
        """)

        login_btn = QPushButton("Already have an account? Log in")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("color: #80dfff; background: transparent; border: none;")
        login_btn.clicked.connect(self.switch_to_login)

        form_layout.addStretch()
        form_layout.addWidget(title)
        form_layout.addSpacing(20)
        form_layout.addWidget(email_input)
        form_layout.addWidget(password_input)
        form_layout.addSpacing(15)
        form_layout.addWidget(signup_btn)
        form_layout.addWidget(google_btn)
        form_layout.addSpacing(10)
        form_layout.addWidget(login_btn)
        form_layout.addStretch()

        form_widget.setLayout(form_layout)

        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addWidget(form_widget)
        outer_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(outer_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
