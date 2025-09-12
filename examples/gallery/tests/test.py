# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, QSize

from PySide6FluentUI import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.showFullScreen()
        self.isHover = False
        self.position = None

        self.viewLayout: QVBoxLayout = QVBoxLayout(self)
        self.roundMenu: RoundMenu = RoundMenu(parent=self)
        self.label: StrongBodyLabel = StrongBodyLabel("Hello World!", self)

        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.addWidget(self.label, 0, Qt.AlignCenter)

        self.geometry = QApplication.primaryScreen().availableGeometry()
        print(self.geometry, QApplication.primaryScreen().size())

        self.roundMenu.addActions([
            Action("Move To LeftButton", self, triggered=lambda: self.move(
                self.geometry.x(), self.geometry.y() + self.geometry.height() - self.height()
            ))
        ])

    def enterEvent(self, event):
        self.isHover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.isHover = False
        self.update()
        super().leaveEvent(event)

    def sizeHint(self):
        return QSize(356, 356)

    def mousePressEvent(self, event):
        self.position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.move(event.globalPosition().toPoint() - self.position)
        super().mouseMoveEvent(event)

    def contextMenuEvent(self, event):
        self.roundMenu.exec(event.globalPos())
        super().contextMenuEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        print('clicked')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 128 if self.isHover else 0))
        painter.drawRoundedRect(self.rect(), 8, 8)


def main():
    app = QApplication(sys.argv)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    window = MainWindow()
    window.setMinimumSize(800, 548)
    window.show()
    sys.exit(app.exec())


main()