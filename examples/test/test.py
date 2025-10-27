# coding:utf-8
import re
import sys

from PySide6.QtCore import QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, Qt
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout

from PySide6FluentUI import PushButton, FluentIcon, SplitWidget, toggleTheme, isDarkTheme, setCustomStyleSheet, \
    drawRoundRect, qconfig, RoundPushButton, RoundToolButton, OutlinePushButton, OutlineToolButton, FillPushButton, \
    FillToolButton


class MainWindow(SplitWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        # toggleTheme()
        self.setMicaEffectEnabled(True)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)

        self.pushButton: PushButton = PushButton(FluentIcon.HOME, "PushButton", self)
        self.roundButton: RoundPushButton = RoundPushButton(FluentIcon.HOME, "RoundButton", self)
        self.trb: RoundToolButton = RoundToolButton(FluentIcon.HOME, self)

        self.outlinePushButton: OutlinePushButton = OutlinePushButton(FluentIcon.HOME, "OutlinePushButton", self)
        self.outlineToolButton: OutlineToolButton = OutlineToolButton(FluentIcon.GITHUB, self)

        self.fillPushButton: FillPushButton = FillPushButton(FluentIcon.ACCEPT, "FillPushButton", self)
        self.fillToolButton: FillToolButton = FillToolButton(FluentIcon.ACCEPT, self)

        self.viewLayout.addWidget(self.pushButton)
        self.viewLayout.addWidget(self.roundButton)
        self.viewLayout.addWidget(self.trb, 0, Qt.AlignHCenter)
        self.viewLayout.addWidget(self.outlinePushButton)
        self.viewLayout.addWidget(self.outlineToolButton)
        self.viewLayout.addWidget(self.fillPushButton)
        self.viewLayout.addWidget(self.fillToolButton)

        self.resize(800, 520)

        self.pushButton.clicked.connect(toggleTheme)
        self.roundButton.clicked.connect(lambda: self.setMicaEffectEnabled(not self.isMicaEffectEnabled()))

        print(min(self.roundButton.width(), self.roundButton.height()) / 2)
        self.roundButton.setRadius(0, 15, 0, 15)
        self.trb.setRadius(15, 0, 15, 0)

        self.outlinePushButton.setRadius(8, 8, 8, 8)
        self.outlinePushButton.setOutlineColor("deeppink")
        self.fillPushButton.setFillColor("")

        self.outlinePushButton.checkedChange.connect(lambda c: print(c))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    ...

if __name__ == '__main__':
    main()