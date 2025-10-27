# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PySide6FluentUI import FillPushButton, ToastInfoBarColor, ToastInfoBarPosition, ToastInfoBar

from examples.window.splitWidget.demo import Interface


class Window(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.box: QVBoxLayout = QVBoxLayout(self)
        self.box.setContentsMargins(11, 38, 11, 11)
        self.button: FillPushButton = FillPushButton("show toast info bar", self)

        self.box.addWidget(self.button)
        self.connectSignalSlot()


    def connectSignalSlot(self):
        super().connectSignalSlot()
        self.button.clicked.connect(
            lambda: {
                ToastInfoBar.success(
                    "Label 1",
                    "Hello World!, Hello Python!, Hello PySide!",
                    parent=self
                )
            }
        )


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

    ...

if __name__ == '__main__':
    main()