from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect, QFrame, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
import sys


class View(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(0, 0, 0, 60))
        painter.setBrush(QColor(243, 243, 243))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)


class ToolTipDemo(QFrame):
    def __init__(self):
        super().__init__()
        self.container = View(self)
        self.setLayout(QHBoxLayout())
        self.containerLayout = QHBoxLayout(self.container)
        self.layout().addWidget(self.container)

        # add shadow
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(25)
        self.shadowEffect.setColor(QColor(0, 0, 0, 60))
        self.shadowEffect.setOffset(0, 5)
        self.container.setGraphicsEffect(self.shadowEffect)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ToolTipDemo()
    win.resize(300, 256)
    win.show()
    sys.exit(app.exec())
