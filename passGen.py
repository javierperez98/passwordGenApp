import sys
import random
import string
from win32api import GetSystemMetrics
from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QLineEdit,
    QSlider,
    QWidget,
    QStyle,
    QLabel
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        screen_w = GetSystemMetrics(0)
        screen_h = GetSystemMetrics(1)
        app_w = 350
        app_h = 215
        # app_h = 500

        # Window styling, sizing and placement
        self.setFixedSize(app_w, app_h)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.move((screen_w - app_w), (screen_h - app_h - 50))

        # Layouts
        outer_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        checkbox_layout = QHBoxLayout()
        slider_layout = QVBoxLayout()
        password_layout = QHBoxLayout()
        generate_layout = QHBoxLayout()
        outer_layout.setSpacing(12)

        # App title
        title_label = QLabel(text="Password Generator")
        title_label.setProperty("class", "title")

        # Closes the app
        close_btn = QPushButton()
        close_btn.setFixedSize(20, 20)
        close_button = QStyle.StandardPixmap.SP_TitleBarCloseButton
        close_icon = self.style().standardIcon(close_button)
        close_btn.setIcon(close_icon)
        close_btn.clicked.connect(QCoreApplication.instance().quit)

        # Options for charcters to add in password
        lower_cb = QCheckBox("Lowercase")
        upper_cb = QCheckBox("Uppercase")
        nums_cb = QCheckBox("Numbers")
        syms_cb = QCheckBox("Symbols")

        # Sets password length
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(10)
        slider.setMaximum(20)

        # Displays slider value
        slider_label = QLabel(text=str(slider.value()))
        slider_label.setProperty("class", "slider-label")
        slider_label.setAlignment(Qt.AlignmentFlag(app_w//2).AlignHCenter)

        # Sets the slider label
        def setLength():
            slider_label.setText(str(slider.value()))
        slider.valueChanged.connect(setLength)

        # Output of createPassword
        password_field = QLineEdit("")
        password_field.setReadOnly(True)
        password_field.setFixedSize(200, 25)
        password_field.setAlignment(Qt.AlignmentFlag(100).AlignHCenter)
        password_layout.setAlignment(Qt.AlignmentFlag(app_w//2).AlignHCenter)

        # Runs toClipboard
        copy_btn = QPushButton("Copy")
        copy_btn.setFixedSize(50, 25)

        # Copy password to clipboard
        def toClipboard():
            if not password_field.text():
                return
            QApplication.clipboard().setText(password_field.text())
        copy_btn.clicked.connect(toClipboard)

        # Runs createPassword
        generate_btn = QPushButton("Generate")
        generate_btn.setFixedSize(100, 30)

        # Create random password
        def createPassword():
            password = []
            length = slider.value()
            checkboxs = [lower_cb.isChecked(), upper_cb.isChecked(),
                         nums_cb.isChecked(), syms_cb.isChecked()]
            if not any(checkboxs):
                return
            charsList = [string.ascii_lowercase,
                         string.ascii_uppercase, string.digits, string.punctuation]
            chars = ""
            for i, option in enumerate(checkboxs):
                if option:
                    password.append(random.choice(charsList[i]))
                    chars += charsList[i]
                    length -= 1
            for i in range(length):
                password.append(random.choice(chars))
            password = "".join(random.sample(password, len(password)))
            password_field.setText(password)
        generate_btn.clicked.connect(createPassword)

        # Appending Widgets
        top_layout.addWidget(title_label)
        top_layout.addWidget(close_btn)
        for i in [lower_cb, upper_cb, nums_cb, syms_cb]:
            checkbox_layout.addWidget(i)
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(slider)
        password_layout.addWidget(copy_btn)
        password_layout.addWidget(password_field)
        generate_layout.addWidget(generate_btn)

        # Appending Layouts
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(checkbox_layout)
        outer_layout.addLayout(slider_layout)
        outer_layout.addLayout(password_layout)
        outer_layout.addLayout(generate_layout)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    # Enables moving of app
    def mousePressEvent(self, event):
        try:
            self.dragPos = event.globalPosition().toPoint()
        except:
            return

    # Enables moving of app
    def mouseMoveEvent(self, event):
        try:
            self.move(
                self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()
        except:
            return


app = QApplication(sys.argv)
app.setStyleSheet("""
QWidget {
  background-color: #121212;
}
.title {
  font-size: 16px;
  font-weight: 800;
  color: #f2e7fd;
}
QCheckBox {
  font-weight: 800;
  color: #616161;
}
QCheckBox::indicator {
  background-color: #1e1e1e;
}
QCheckBox::indicator:hover {
  background-color: #664b85;
}
QCheckBox::indicator:checked {
  background-color: #bb86fc;
}
.slider-label {
  font-weight: 800;
  color: #616161;
}
QSlider::groove:horizontal {
  background-color: #1e1e1e;
  height: 10px;
}
QSlider::handle:horizontal {
  background-color: #bb86fc;
  margin: -5px 0px;
  width: 10px;
}
QLineEdit {
  background-color: #1e1e1e;
  font-weight: 800;
  color: #616161;
  border: none;
}
QPushButton {
  background-color: #bb86fc;
  font-weight: 800;
  color: #121212;
  border: none;
}
QPushButton:pressed {
  background-color: #664b85;
}
""")
window = MainWindow()
window.show()
app.exec()
