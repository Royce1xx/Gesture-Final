import sys
from PyQt5.QtWidgets import QApplication
from auth.signup import SignUpWindow
from auth.login import LoginWindow

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.signup_window = SignUpWindow(self.show_login)
        self.login_window = LoginWindow(self.show_signup)

        self.current_window = self.signup_window
        self.current_window.show()

    def show_login(self):
        self.current_window.hide()
        self.current_window = self.login_window
        self.current_window.show()

    def show_signup(self):
        self.current_window.hide()
        self.current_window = self.signup_window
        self.current_window.show()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = AppController()
    controller.run()
