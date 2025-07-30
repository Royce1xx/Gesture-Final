import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap


class TrainGestureWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Train New Gestures")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #0d1117; color: white;")

        # Layout
        layout = QVBoxLayout()

        # Webcam preview
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.video_label)

        # Exit button
        self.exit_btn = QPushButton("Back to Home")
        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #80dfff;
                padding: 10px;
                color: black;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #a5e8ff;
            }
        """)
        self.exit_btn.clicked.connect(self.close)
        layout.addWidget(self.exit_btn)

        self.setLayout(layout)

        # OpenCV webcam setup
        self.cap = cv2.VideoCapture(0)

        # QTimer to update frame
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb.shape
            bytes_per_line = ch * w
            image = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pix = QPixmap.fromImage(image)
            self.video_label.setPixmap(pix)

    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrainGestureWindow()
    window.show()
    sys.exit(app.exec_())
