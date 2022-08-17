import sys
from win32api import GetSystemMetrics
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,

)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        screen_w = GetSystemMetrics(0)
        screen_h = GetSystemMetrics(1)
        app_w = 350
        app_h = 500

        # Window styling, sizing and placement
        self.setFixedSize(app_w, app_h)
        self.move((screen_w - app_w), (screen_h - app_h - 50))

        # Layouts
        outer_layout = QVBoxLayout()
        outer_layout.addStretch()
        self.setLayout(outer_layout)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
