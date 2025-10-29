# coding:utf-8
import sys

from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter, QColor, Qt, QPen
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton

from PySide6FluentUI import setCustomStyleSheet, LineEdit, isDarkTheme, FocusLineEdit
from examples.window.splitWidget.demo import Interface


class Window(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.focusLineEdit: FocusLineEdit = FocusLineEdit(self)
        self.button: QPushButton = QPushButton(self)

        self.focusLineEdit.setCustomFocusedBorderColor("deeppink", "deepskyblue")

        self.connectSignalSlot()

        self.viewLayout.addWidget(self.focusLineEdit)
        self.viewLayout.addWidget(self.button)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()