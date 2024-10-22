from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        pallete = self.palette()
        pallete.setColor(QPalette.Window, QColor(color))
        self.setPalette(pallete)