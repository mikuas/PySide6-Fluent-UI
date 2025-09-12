# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, \
    QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation

from PySide6FluentUI import ToolTip, ToolTipPosition, setToolTipInfo


class ToolTip(QFrame):
    def __init__(self, text='', parent=None):
        super().__init__(parent=parent)
        self.__text = text
        self.__duration = 1000

        self.container = self._createContainer()

        self.setLayout(QHBoxLayout())
        self.containerLayout = QHBoxLayout(self.container)
        self.label = QLabel(text, self)

        # set layout
        self.layout().setContentsMargins(12, 8, 12, 12)
        self.layout().addWidget(self.container)
        self.containerLayout.addWidget(self.label)
        self.containerLayout.setContentsMargins(8, 6, 8, 6)

        # add shadow
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(25)
        self.shadowEffect.setColor(QColor(0, 0, 0, 60))
        self.shadowEffect.setOffset(0, 5)
        self.container.setGraphicsEffect(self.shadowEffect)

        # set style
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)


def main():
    app = QApplication(sys.argv)
    window = ToolTip("hello world")
    window.resize(300, 256)
    window.show()
    sys.exit(app.exec())
    ...


if __name__ == '__main__':
    main()