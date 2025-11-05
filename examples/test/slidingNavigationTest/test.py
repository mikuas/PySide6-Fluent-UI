# coding:utf-8
import sys
from typing import List, Dict, Any

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QColor, QIntValidator
from PySide6.QtCore import Qt

from PySide6FluentUI import SlidingNavigationBar, FillPushButton, FluentIcon, FocusLineEdit, TransparentTogglePushButton

from sliding_navigation_bar_test import SlidingToolNavigationBar, SlidingWidget
from examples.window.splitWidget.demo import Interface


class SlidingNavigationBarInterface(Interface):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.box: QVBoxLayout = QVBoxLayout(self)
        self.box.setContentsMargins(12, 35, 12, 12)

        self.slidingNavigationBar: SlidingNavigationBar = SlidingNavigationBar(self)
        self.button: TransparentTogglePushButton = TransparentTogglePushButton(FluentIcon.EDIT, "编辑", self)

        items: List[Dict[str, Any]] = [
            {"routeKey": "HOME", "Text": "HOME", "Icon": FluentIcon.HOME, "onClicked": None, "isSelected": True, "toolTip": "HOME Interface"},
            {"routeKey": "GITHUB", "Text": "GITHUB", "Icon": FluentIcon.GITHUB, "onClicked": None, "isSelected": False, "toolTip": "GITHUB Interface"},
            {"routeKey": "VIDEOS", "Text": "VIDEOS", "Icon": FluentIcon.VIDEO, "onClicked": None, "isSelected": False, "toolTip": "VIDEOS Interface"},
            {"routeKey": "MUSIC", "Text": "MUSIC", "Icon": FluentIcon.MUSIC, "onClicked": None, "isSelected": False, "toolTip": "MUSIC Interface"},
            {"routeKey": "HELP", "Text": "HELP", "Icon": FluentIcon.HELP, "onClicked": None, "isSelected": False, "toolTip": "HELP Interface"},
            {"routeKey": "SETTING", "Text": "", "Icon": FluentIcon.SETTING, "onClicked": None, "isSelected": False, "toolTip": "SETTING Interface"},
        ]

        for item in items:
            if item["routeKey"] == "MUSIC":
                self.slidingNavigationBar.addWidget(self.button)
                self.slidingNavigationBar.addSeparator()
            self.slidingNavigationBar.addItem(
                item["routeKey"], item["Text"], item["Icon"], item["onClicked"], item["isSelected"], item["toolTip"]
            )


        for i in range(1, 10001):
            self.slidingNavigationBar.addItem(f"Item {i}", f"Item {i}", toolTip=f"Item{i} Interface")
        # self.slidingNavigationBar.removeItem("SETTING")

        self.box.addWidget(self.slidingNavigationBar)

        self.buttonLayout: QHBoxLayout = QHBoxLayout()
        self.box.addLayout(self.buttonLayout)

        self.setCurrentIndexEdit: FocusLineEdit = FocusLineEdit(self)
        self.getRouteKeyButton: FillPushButton = FillPushButton("获取 routeKey", self)
        self.getCurrentItemButton: FillPushButton = FillPushButton("获取当前Item", self)
        self.getAllItemButton: FillPushButton = FillPushButton("获取所有Item", self)

        self.buttonLayout.addWidget(self.setCurrentIndexEdit)
        self.buttonLayout.addWidget(self.getRouteKeyButton)
        self.buttonLayout.addWidget(self.getCurrentItemButton)
        self.buttonLayout.addWidget(self.getAllItemButton)

        self.setCurrentIndexEdit.setPlaceholderText("设置当前Index")
        self.setCurrentIndexEdit.setValidator(QIntValidator(self))
        self.getRouteKeyButton.setFillColor("#15b169")
        self.getAllItemButton.setFillColor("#d29b58")

        self.connectSignalSlot()

    def _onCurrentItemChanged(self, item: SlidingWidget):
        print(f"{item.text() = }\n{item.icon() = }\n{item.iconSize() = }\n{item.itemColor() = }\n{item.itemHoverColor() = }"
              f"\n{item.itemSelectedColor() = }\n\n\n")

    def _onClickedGetRouteKeyButton(self):
        print(f"RouteKey: {self.slidingNavigationBar.currentItem().routeKey()}")

    def _onClickedGetCurrentItemButton(self):
        print(f"CurrentItem: {self.slidingNavigationBar.currentItem()}")

    def _onClickedGetAllItemButton(self):
        print(f"AllItem: {[item.routeKey() for item in self.slidingNavigationBar.allItem()]}")

    def _onReturnPressedEdit(self):
        self.slidingNavigationBar.setCurrentIndex(int(self.setCurrentIndexEdit.text()))
        self.slidingNavigationBar.hScrollBar.scrollTo(self.slidingNavigationBar.currentItem().pos().x(), True)

    def connectSignalSlot(self):
        super().connectSignalSlot()
        self.slidingNavigationBar.currentItemChanged.connect(self._onCurrentItemChanged)

        self.setCurrentIndexEdit.returnPressed.connect(self._onReturnPressedEdit)
        self.getRouteKeyButton.clicked.connect(self._onClickedGetRouteKeyButton)
        self.getCurrentItemButton.clicked.connect(self._onClickedGetCurrentItemButton)
        self.getAllItemButton.clicked.connect(self._onClickedGetAllItemButton)


def main():
    app = QApplication(sys.argv)
    window = SlidingNavigationBarInterface()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())

    ...

if __name__ == '__main__':
    main()