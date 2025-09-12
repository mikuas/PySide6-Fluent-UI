# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from PySide6FluentUI import ScreenColorPicker, themeColor
from examples.wiindow.splitWidget.demo import Interface


class Window(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.box: QVBoxLayout = QVBoxLayout(self)
        self.screenColorPicker: ScreenColorPicker = ScreenColorPicker(self)

        self.screenColorPicker.setDefaultColor(themeColor())
        self.box.addWidget(self.screenColorPicker, 0, Qt.AlignCenter)
        self.connectSignalSlot()

    def connectSignalSlot(self):
        super().connectSignalSlot()
        self.screenColorPicker.colorChanged.connect(
            lambda color: print(
                color, self.screenColorPicker.currentColor()
            )
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