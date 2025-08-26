# coding:utf-8
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget

from ..layout import VBoxLayout, HBoxLayout
from .pips_pager import PipsPager, PipsScrollButtonDisplayMode
from .stacked_widget import PopUpAniStackedWidget


class PagerWidgetBase(QWidget):
    """ pager widget base class """

    def __init__(self, parent=None, orientation=Qt.Orientation.Vertical):
        super().__init__(parent)
        self.__toggle = True
        self._pager = PipsPager(orientation, self)
        self._stackedWidget = PopUpAniStackedWidget(self)
        self._pager.currentIndexChanged.connect(lambda index: self._stackedWidget.setCurrentIndex(index))
        self.__widgets = []  # type: [QWidget]

    def addWidget(self, widget: QWidget):
        """ add widget to stacked widget """
        self._stackedWidget.addWidget(widget)
        self._addToWidgets(widget)
        self._pager.setPageNumber(len(self.getAllWidget()))
        return self

    def addWidgets(self, widgets: list[QWidget]):
        """ add widgets to stacked widget """
        for widget in widgets:
            self.addWidget(widget)
        return self

    def setCurrentIndex(self, index: int):
        """ set current page index """
        self._pager.setCurrentIndex(index)

    def removeWidget(self, index: int):
        """ remove widget from stacked widget """
        if index < len(self.__widgets):
            self._stackedWidget.removeWidget(self.__widgets.pop(index))
            self._pager.setPageNumber(len(self.__widgets))
        return self

    def _addToWidgets(self, widget: QWidget):
        if widget in self.__widgets:
            return
        self.__widgets.append(widget)

    def enableScrollTogglePage(self, enable: bool):
        self.toggle = enable

    def displayNextButton(self):
        """ set next page button display """
        self._pager.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)

    def displayPrevButton(self):
        """ set previous page button display """
        self._pager.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)

    def hoverDisplayPrevButton(self):
        """ set previous page button hover display """
        self._pager.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ON_HOVER)

    def hoverDisplayNextButton(self):
        """ set next page button hover display """
        self._pager.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ON_HOVER)

    def setPageVisible(self, visible: bool):
        """ set page visible flag """
        self._pager.setVisible(visible)

    def setVisibleNumber(self, number: int):
        """ set page visible flag """
        self._pager.setVisibleNumber(number)

    def setStackedFixedSize(self, width: int, height: int):
        self._stackedWidget.setFixedSize(width, height)

    def setStackedMinSize(self, width: int, height: int):
        self._stackedWidget.setMinimumSize(width, height)

    def pageNumber(self):
        return self._pager.getPageNumber()

    def getAllWidget(self):
        """ get stacked all widget """
        return self.__widgets

    def _initLayout(self):
        self.__layout = HBoxLayout(self)
        self.__layout.addWidget(self._stackedWidget)
        self.__layout.addWidget(self._pager, alignment=Qt.AlignmentFlag.AlignRight)

    def getCurrentIndex(self):
        return self._pager.currentIndex()

    def wheelEvent(self, event):
        super().wheelEvent(event)
        if self.__toggle:
            index = self.getCurrentIndex()
            if event.angleDelta().y() > 0:
                if index == 0:
                    return
                self.setCurrentIndex(index - 1)
            else:
                if index == self.getPageNumber() - 1:
                    return
                self.setCurrentIndex(index + 1)


class VerticalPagerWidget(PagerWidgetBase):
    """ 垂直分页器 """

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Orientation.Horizontal)
        self._initLayout()

    def addWidget(self, widget: QWidget, deltaX=76, deltaY=0):
        """ add widget to stacked widget """
        self._stackedWidget.addWidget(widget, deltaX, deltaY)
        self._addToWidgets(widget)
        self._pager.setPageNumber(len(self.getAllWidget()))
        return self

    def _initLayout(self):
        self.__layout = VBoxLayout(self)
        self.__layout.addWidget(self._stackedWidget)
        self.__layout.addWidget(self._pager, alignment=Qt.AlignmentFlag.AlignHCenter)


class HorizontalPagerWidget(PagerWidgetBase):
    """ 水平分页器 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._initLayout()
