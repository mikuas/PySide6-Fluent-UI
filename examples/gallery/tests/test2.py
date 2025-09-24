from PySide6.QtWidgets import QWidget, QApplication, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QPainterPath
from PySide6.QtCore import Qt, QRectF, QStringListModel
import sys

from PySide6FluentUI import *
from examples.gallery.app.common.config import update


class Window(SplitWidget):
    def __init__(self):
        super().__init__()
        self.box: QVBoxLayout = QVBoxLayout(self)
        self.box.setContentsMargins(11, 38, 11, 11)
        self.toggleThemeButton: TransparentToolButton = TransparentToolButton(FluentIcon.BROOM, self)
        self.toggleThemeButton.setFixedSize(46, 32)
        self.titleBar.hBoxLayout.insertWidget(4, self.toggleThemeButton)
        self.toggleThemeButton.clicked.connect(lambda: {toggleTheme(), update()})

        self.colorPicker: ScreenColorPicker = ScreenColorPicker(self)
        self.dropDownColorPalette: DropDownColorPalette = DropDownColorPalette(self)
        self.roundListWidget: RoundListWidget = RoundListWidget(self)
        self.roundListView: RoundListView = RoundListView(self)

        model = QStringListModel()
        model.setStringList([f"Item {_}" for _ in range(1, 11)])
        self.roundListView.setModel(model)
        # self.roundListView.setStyleSheet("RoundListView {background: transparent; border: none;}")

        self.roundListWidget.addItems([f"Item {_}" for _ in range(1, 11)])

        self.box.addWidget(self.colorPicker, 0, Qt.AlignHCenter)
        self.box.addWidget(self.dropDownColorPalette, 0, Qt.AlignHCenter)
        self.box.addWidget(self.roundListView)
        self.box.addWidget(self.roundListWidget)
        self.box.setAlignment(Qt.AlignCenter)

        self.colorPicker.colorChanged.connect(print)
        self.dropDownColorPalette.colorChanged.connect(print)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
