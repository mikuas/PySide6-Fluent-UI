# coding:utf-8
import sys

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication

from PySide6FluentUI import FluentIcon


def main():

    class Window(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)

            self.setLayout(QVBoxLayout())

            self.icon = FluentIcon.HOME.colored(QColor("deeppink"), QColor("deeppink"))
            self.button: QPushButton = QPushButton(self)

            self.button.setIcon(self.icon.icon(color=QColor("deeppink")))

            self.layout().addWidget(self.button)

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
    ...

if __name__ == '__main__':
    main()