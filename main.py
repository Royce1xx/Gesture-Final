from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class SignUpWindow(QWidget):
    def __init__(self):
        super().__init__()

        print("program running")

        self.setWindowTitle("Gesture Controller - Sign Up")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #0d1117;")

        # 🌟 Signup form (center widget)
        form_widget = QWidget()
        form_widget.setFixedWidth(350)

        form_layout = QVBoxLayout()

        # Title
        title = QLabel("Sign Up")
        title.setFont(QFont("Arial", 24))
        title.setStyleSheet("color: #80dfff;")
        title.setAlignment(Qt.AlignCenter)

        # Email input
        email_input = QLineEdit()
        email_input.setPlaceholderText("Email")
        email_input.setStyleSheet("padding: 10px; background-color: #1e222a; border: 1px solid #80dfff; color: white;")

        # Password input
        password_input = QLineEdit()
        password_input.setPlaceholderText("Password")
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setStyleSheet("padding: 10px; background-color: #1e222a; border: 1px solid #80dfff; color: white;")

        # Buttons
        signup_button = QPushButton("Sign Up")
        signup_button.setStyleSheet("background-color: #80dfff; padding: 10px; font-weight: bold; border-radius: 5px;")

        google_button = QPushButton("Sign Up with Google")
        google_button.setStyleSheet("background-color: white; padding: 10px; color: black; border-radius: 5px;")

        login_label = QLabel("Already have an account?")
        login_label.setStyleSheet("color: white;")
        login_label.setAlignment(Qt.AlignCenter)

        # Add widgets to form layout
        form_layout.addWidget(title)
        form_layout.addSpacing(20)
        form_layout.addWidget(email_input)
        form_layout.addWidget(password_input)
        form_layout.addSpacing(10)
        form_layout.addWidget(signup_button)
        form_layout.addWidget(google_button)
        form_layout.addSpacing(10)
        form_layout.addWidget(login_label)

        form_widget.setLayout(form_layout)

        # 🌟 Outer layout to center form
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
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = SignUpWindow()
    window.show()
    sys.exit(app.exec_())
