# coding:utf-8
import re
import sys

from PySide6.QtCore import QRectF, QTimer
from PySide6.QtGui import QPainter, QColor, Qt
from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout

from PySide6FluentUI import PushButton, FluentIcon, SplitWidget, toggleTheme, isDarkTheme, setCustomStyleSheet, \
    drawRoundRect, qconfig, RoundPushButton


# class RoundPushButton(PushButton):
#
#     def _postInit(self):
#         super()._postInit()
#         self.tl, self.tr, self.bl, self.br = 12, 12, 12, 12
#         qconfig.themeChangedFinished.connect(self.__updateRadius)
#
#     def __updateRadius(self):
#         qss = self.styleSheet()
#         radius = {
#             "top-left": self.tl,
#             "top-right": self.tr,
#             "bottom-left": self.bl,
#             "bottom-right": self.br
#         }
#         for i in ["top", "bottom"]:
#             for j in ["left", "right"]:
#                 qss = re.sub(fr"border-{i}-{j}-radius:\s*\d+px;", f"border-{i}-{j}-radius: {radius[f"{i}-{j}"]}px;", qss)
#
#         print(qss)
#         self.setStyleSheet(qss)
#
#     def paintEvent(self, e):
#         super().paintEvent(e)
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.RenderHint.Antialiasing)
#         painter.setPen(QColor(255, 255, 255, 32) if isDarkTheme() else QColor(32, 32, 32, 16))
#         painter.setBrush(Qt.NoBrush)
#         drawRoundRect(painter, QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5), *self.radius())
#
#     def radius(self):
#         return self.tl, self.tr, self.br, self.bl
#
#     def setRadius(self, tl: int, tr: int, br: int, bl: int):
#         r = min(self.width(), self.height()) / 2
#         if tl > r or tr > r or br > r or bl > r:
#             return
#         self.tl, self.tr, self.br, self.bl = tl, tr, br, bl
#         self.__updateRadius()


class MainWindow(SplitWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        toggleTheme()
        self.setMicaEffectEnabled(True)
        self.viewLayout: QVBoxLayout = QVBoxLayout(self)

        self.pushButton: PushButton = PushButton(FluentIcon.HOME, "PushButton", self)
        self.roundButton: RoundPushButton = RoundPushButton(FluentIcon.HOME, "RoundButton", self)

        self.viewLayout.addWidget(self.pushButton)
        self.viewLayout.addWidget(self.roundButton)

        self.resize(800, 520)

        self.pushButton.clicked.connect(toggleTheme)
        self.roundButton.clicked.connect(lambda: self.setMicaEffectEnabled(not self.isMicaEffectEnabled()))

        print(min(self.roundButton.width(), self.roundButton.height()) / 2)
        self.roundButton.setRadius(16, 16, 16, 16)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    ...

if __name__ == '__main__':
    main()