# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QSplitter, QSplitterHandle, QTextEdit, QVBoxLayout
from PySide6.QtCore import Qt, QSize, QRectF, QStringListModel, QPoint
from PySide6.QtGui import QPainter, QColor
from PySide6FluentUI import RoundListView, isDarkTheme, RoundListWidget, Splitter, PopupView

from examples.wiindow.splitWidget.demo import Interface


class Window(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.popupView: PopupView = PopupView(self)
        self.popupView.setFixedSize(256, 256)
        self.connectSignalSlot()

    def connectSignalSlot(self):
        super().connectSignalSlot()

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        pos = event.globalPos()
        self.popupView.exec(pos - QPoint(0, 24), pos)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

    ...

if __name__ == '__main__':
    main()
