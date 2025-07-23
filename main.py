import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve


class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gesture Controller - Sign Up")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #0d1117;")

        # 🌟 Glowing card container
        form_widget = QWidget()
        form_widget.setFixedWidth(380)
        form_widget.setStyleSheet("""
            background-color: #1b1f27;
            border-radius: 16px;
        """)

        # Add glow shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(50)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(128, 223, 255))
        form_widget.setGraphicsEffect(shadow)

        # Add animated pulsing glow
        self.glow_anim = QPropertyAnimation(shadow, b"blurRadius")
        self.glow_anim.setStartValue(40)
        self.glow_anim.setEndValue(70)
        self.glow_anim.setDuration(1500)
        self.glow_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.glow_anim.setLoopCount(-1)
        self.glow_anim.start()

        # Layout inside form
        form_layout = QVBoxLayout()

        title = QLabel("Sign Up")
        title.setFont(QFont("Arial", 26))
        title.setStyleSheet("color: #80dfff;")
        title.setAlignment(Qt.AlignCenter)

        email_input = QLineEdit()
        email_input.setPlaceholderText("Email")
        email_input.setStyleSheet("""
            padding: 12px;
            background-color: #0e1016;
            border: 1px solid #80dfff;
            border-radius: 8px;
            color: white;
        """)

        password_input = QLineEdit()
        password_input.setPlaceholderText("Password")
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setStyleSheet("""
            padding: 12px;
            background-color: #0e1016;
            border: 1px solid #80dfff;
            border-radius: 8px;
            color: white;
        """)

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

        login_label = QLabel("Already have an account?")
        login_label.setStyleSheet("color: #b0b0b0; font-size: 13px;")
        login_label.setAlignment(Qt.AlignCenter)

        form_layout.addStretch()
        form_layout.addWidget(title)
        form_layout.addSpacing(20)
        form_layout.addWidget(email_input)
        form_layout.addWidget(password_input)
        form_layout.addSpacing(15)
        form_layout.addWidget(signup_btn)
        form_layout.addWidget(google_btn)
        form_layout.addSpacing(10)
        form_layout.addWidget(login_label)
        form_layout.addStretch()

        form_widget.setLayout(form_layout)

        # Center it
        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addWidget(form_widget)
        outer_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(outer_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignUpWindow()
    window.show()
    sys.exit(app.exec_())
