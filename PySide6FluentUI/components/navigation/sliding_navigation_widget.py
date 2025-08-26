# coding:utf-8
from typing import Union

from PySide6.QtWidgets import QWidget, QVBoxLayout

from ...common.icon import FluentIcon
from .sliding_navigation_bar import SlidingNavigationBar
from ..widgets.stacked_widget import PopUpAniStackedWidget


class SlidingNavigationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widgetLayout: QVBoxLayout = QVBoxLayout(self)
        self.navigation: SlidingNavigationBar = SlidingNavigationBar(self)
        self.stackedWidget: PopUpAniStackedWidget = PopUpAniStackedWidget(self)
        self.__initLayout()

    def __initLayout(self) -> None:
        self.widgetLayout.addWidget(self.navigation)
        self.widgetLayout.addWidget(self.stackedWidget)

    def _switchTo(self, widget: QWidget) -> None:
        self.stackedWidget.setCurrentWidget(widget)

    def setCurrentWidget(self, item: Union[str, QWidget]) -> None:
        if isinstance(item, QWidget):
            item = item.property("routeKey")
        self.navigation.setCurrentWidget(item)

    def setCurrentIndex(self, index: int) -> None:
        self.navigation.setCurrentIndex(index)

    def addSubInterface(self, routeKey: str, text: str, widget: QWidget, icon: FluentIcon = None, toolTip=None) -> None:
        widget.setProperty("routeKey", routeKey)
        self.navigation.addItem(routeKey, text, icon, lambda: self._switchTo(widget), toolTip=toolTip)
        self.stackedWidget.addWidget(widget)

    def removeSubInterface(self, widget: QWidget) -> None:
        item = self.navigation.removeItem(widget.property("routeKey"))
        if item:
            item.deleteLater()
        self.stackedWidget.removeWidget(widget)
