# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QSplitter, QSplitterHandle, QTextEdit, QVBoxLayout
from PySide6.QtCore import Qt, QSize, QRectF, QStringListModel
from PySide6.QtGui import QPainter, QColor
from PySide6FluentUI import RoundListView, isDarkTheme, RoundListWidget, Splitter

from examples.wiindow.splitWidget.demo import Interface


class Window(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(11, 38, 11, 11)
        self.splitter: Splitter = Splitter(Qt.Orientation.Horizontal, self)

        self.roundList1: RoundListWidget = RoundListWidget(self)
        self.roundList1.addItems([f"Item {_}" for _ in range(1, 101)])
        self.roundList1.setItemBorderColor("deepskyblue")

        self.roundList2: RoundListView = RoundListView(self)
        self.roundList2.setModel(QStringListModel([f"Item {_}" for _ in range(1, 101)]))
        self.roundList2.setItemBorderColor("deeppink")

        self.splitter.addWidget(self.roundList1)
        self.splitter.addWidget(self.roundList2)
        self.box.addWidget(self.splitter)

        self.connectSignalSlot()
    
    def connectSignalSlot(self):
        super().connectSignalSlot()


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

    ...

if __name__ == '__main__':
    main()
