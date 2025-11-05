# coding:utf-8
from typing import Union, List, Dict, Tuple

from PySide6.QtWidgets import QWidget, QFrame, QHBoxLayout
from PySide6.QtCore import Qt, QRect, Signal, QPropertyAnimation, QPoint, QTimer, QEvent, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QFontMetrics, QPen, QIcon


from PySide6FluentUI import themeColor, isDarkTheme, setFont, FluentIcon, FluentIconBase, setToolTipInfo, ToolTipPosition, \
    SingleDirectionScrollArea
from PySide6FluentUI.common.icon import toQIcon
from PySide6FluentUI.components.navigation.navigation_panel import RouteKeyError


class SlidingWidget(QWidget):

    clicked = Signal(QWidget)

    def __init__(self, text: str, icon: FluentIconBase = None, isSelected=False, parent=None) -> None:
        super().__init__(parent)
        setFont(self, 16)
        self.isHover: bool = False
        self.isSelected: bool = isSelected
        self._text: str = text
        self._icon: Union[FluentIcon, None] = None
        self._itemColor: Union[FluentIcon, None] = None
        self._hoverColor: Union[FluentIcon, None] = None
        self._selectedColor: Union[FluentIcon, None] = None
        self._lastColor: Union[FluentIcon, None] = None
        self._iconSize: int = 16
        self._fontMetrics: QFontMetrics = QFontMetrics(self.font())
        self._adjustSize()
        self.setIcon(icon)

    def _adjustSize(self, size=0) -> None:
        self.setMinimumSize(self._fontMetrics.horizontalAdvance(self._text) + 12 + size, 35)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.isHover = True
        self.update()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.isHover = False
        self.update()

    def mouseReleaseEvent(self, event) -> None:
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton and self.isHover:
            self.clicked.emit(self)

    def setSelected(self, isSelected: bool) -> None:
        self.isSelected = isSelected
        self.update()

    def setText(self, text: str) -> None:
        self._text = text
        self._adjustSize()
        self.update()

    def setIcon(self, icon: FluentIconBase) -> None:
        self._icon = icon or QIcon()
        self._adjustSize(self._iconSize * 2)
        self.update()

    def setIconSize(self, size: int) -> None:
        if self._iconSize == size:
            return
        self._iconSize = size
        self.update()

    def setItemColor(self, color: Union[str, QColor]) -> None:
        if self._itemColor == color:
            return
        self._itemColor = color
        self.update()

    def setItemHoverColor(self, color: Union[str, QColor]) -> None:
        if self._hoverColor == color:
            return
        self._hoverColor = color
        self.update()

    def setItemSelectedColor(self, color: Union[str, QColor]) -> None:
        if self._selectedColor == color:
            return
        self._selectedColor = color
        self.update()

    def click(self):
        self.clicked.emit(self)

    def icon(self) -> QIcon:
        return toQIcon(self._icon)

    def text(self) -> str:
        return self._text

    def iconSize(self) -> int:
        return self._iconSize

    def itemColor(self) -> Union[QColor, None]:
        return self._itemColor or (QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0))

    def itemHoverColor(self) -> Union[QColor, None]:
        return self._hoverColor or themeColor()

    def itemSelectedColor(self) -> Union[QColor, None]:
        return self._selectedColor or themeColor()

    def routeKey(self) -> str:
        return self.property("routeKey")

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        rect = self.rect()
        alignment = Qt.AlignCenter
        if self.isSelected:
            color = self.itemSelectedColor()
        elif self.isHover:
            color = self.itemHoverColor()
        else:
            color = self.itemColor()
        if not self.icon().isNull():
            rect, alignment = self._drawIcon(color, painter, rect)
        self._drawText(color, painter, rect, alignment)

    def _drawIcon(self, color: QColor, painter: QPainter, rect: QRect) -> Tuple[QRect, Qt.AlignmentFlag]:
        if isinstance(self._icon, FluentIconBase) and self._lastColor != color:
            self._icon = self._icon.colored(color, color)
            self._lastColor = QColor(color)
        x = (self.width() - self._fontMetrics.horizontalAdvance(self._text) - self._iconSize) / 2
        y = (self.height() - self._iconSize) / 2
        self._icon.render(painter, QRect(x, y, self._iconSize, self._iconSize))
        rect.adjust(x + self._iconSize + 6, 0, 0, 0)
        return rect, Qt.AlignVCenter

    def _drawText(self, color: QColor, painter: QPainter, rect: QRect, alignment: Qt.AlignmentFlag) -> None:
        painter.setPen(color)
        painter.drawText(rect, alignment, self._text)


class SlidingLine(QFrame):

    def __init__(self, parent=None, color: QColor = None, height=4) -> None:
        super().__init__(parent)
        self.setFixedHeight(height)
        self._color: QColor = color

    def setLineColor(self, color: Union[str, QColor]) -> None:
        if isinstance(color, str):
            color = QColor(color)
        if color == self.color():
            return
        self._color = color
        self.update()

    def color(self) -> QColor:
        return self._color

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self._color or themeColor())
        painter.drawRoundedRect(self.rect(), 2, 2)


class SmoothSeparator(QWidget):
    """ Smooth Switch Separator """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedWidth(6)
        self._color: QColor = None

    def setSeparatorColor(self, color: Union[str, QColor]) -> None:
        if isinstance(color, str):
            color = QColor(color)
        self._color = color
        self.update()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = 255 if isDarkTheme() else 0
        pen = QPen(self._color or QColor(color, color, color, 128), 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(2, 10, 2, self.height() - 10)


class SlidingNavigationBar(SingleDirectionScrollArea):

    currentItemChanged: Signal = Signal(SlidingWidget)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent, Qt.Horizontal)
        self.setFixedHeight(60)
        self._items: Dict[str, SlidingWidget] = {}
        self.__currentItem: SlidingWidget = None

        self._widget: QWidget = QWidget()
        self._widget.setStyleSheet("background:transparent;")

        self._widgetLayout: QHBoxLayout = QHBoxLayout(self._widget)

        self._slidingLine: SlidingLine = SlidingLine(self._widget)
        self.__slideLineWidth: int = 30
        self._slidingLine.setFixedSize(self.__slideLineWidth, 3)
        self._slidingLine.raise_()

        self.__posAni: QPropertyAnimation = QPropertyAnimation(self._slidingLine, b"pos")
        self.__posAni.setEasingCurve(QEasingCurve.OutCubic)

        self.__initScrollArea()
        parent.installEventFilter(self)

    def __initScrollArea(self) -> None:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.enableTransparentBackground()
        self.setWidgetResizable(True)
        self.setWidget(self._widget)

    def __getSlideEndPos(self, item: SlidingWidget) -> QPoint:
        pos = item.pos()
        x = pos.x()
        y = pos.y()
        width = item.width()
        height = item.height()
        return QPoint(x + width // 2 - self.__slideLineWidth // 2, y + height)

    def __createPosAni(self, item: SlidingWidget) -> None:
        self.__posAni.setDuration(200)
        self.__posAni.setStartValue(self._slidingLine.pos())
        self.__posAni.setEndValue(self.__getSlideEndPos(item))
        self.__posAni.start()

    def __make(self, name: str, *args, **kwargs) -> None:
        for item in self._items.values():
            method = getattr(item, name, None)
            if callable(method):
                method(*args, **kwargs)

    def _adjustSlideLinePos(self) -> None:
        try:
            self._slidingLine.move(self.__getSlideEndPos(self.__currentItem))
        except AttributeError:
            return

    def _onClicked(self, item: SlidingWidget) -> None:
        self.setCurrentWidget(item)

    def setEasingCurve(self, easing: QEasingCurve.Type) -> None:
        self.__posAni.setEasingCurve(easing)

    def setBarAlignment(self, alignment: Qt.AlignmentFlag) -> None:
        self._widgetLayout.setAlignment(alignment)

    def addSeparator(self) -> SmoothSeparator:
        return self.insertSeparator(-1)

    def insertSeparator(self, index: int) -> SmoothSeparator:
        separator = SmoothSeparator(self)
        self._widgetLayout.insertWidget(index, separator)
        return separator

    def setSlideLineWidth(self, width: int) -> None:
        self.__slideLineWidth: int = width
        self._slidingLine.setFixedWidth(self.__slideLineWidth)
        self._adjustSlideLinePos()

    def setSlideLineColor(self, color: Union[str, QColor]) -> None:
        self._slidingLine.setLineColor(color)

    def setItemSelectedColor(self, color: Union[str, QColor]) -> None:
        self.__make("setItemSelectedColor", color)

    def setItemColor(self, color: Union[str, QColor]) -> None:
        self.__make("setItemColor", color)

    def setItemHoverColor(self, color: Union[str, QColor]) -> None:
        self.__make("setItemHoverColor", color)

    def setItemSize(self, width: int, height: int) -> None:
        self.__make("setFixedSize", width, height)

    def setCurrentWidget(self, item: Union[str, SlidingWidget]) -> None:
        values = self._items.values()
        if isinstance(item, str):
            if item not in self._items:
                return
            item = self._items[item]
        if item not in values or item is self.__currentItem:
            return
        for obj in values:
            obj.setSelected(False)
        self.currentItemChanged.emit(item)
        self.__currentItem = item
        item.setSelected(True)
        item.click()
        QTimer.singleShot(1, lambda: self.__createPosAni(item))

    def setCurrentIndex(self, index: int) -> None:
        if index >= len(self._items.keys()) or index < 0:
            return
        self.setCurrentWidget(list(self._items.keys())[index])

    def addStretch(self, stretch: int) -> None:
        self._widgetLayout.addStretch(stretch)

    def addSpacing(self, size: int) -> None:
        self._widgetLayout.addSpacing(size)

    def addItem(
            self,
            routeKey: str,
            text: str,
            icon: FluentIcon = None,
            onClick=None,
            isSelected=False,
            toolTip: str = None
    ) -> None:
        self.insertItem(-1, routeKey, text, icon, onClick, isSelected, toolTip)

    def insertItem(
            self,
            index: int,
            routeKey: str,
            text: str,
            icon: FluentIcon = None,
            onClick=None,
            isSelected=False,
            toolTip: str = None
    ) -> None:
        if routeKey in self._items:
            raise RouteKeyError('routeKey Are Not Unique')
        item = SlidingWidget(text, icon, isSelected, self._widget)
        item.setProperty("routeKey", routeKey)
        self._widgetLayout.insertWidget(index, item)
        self._items[routeKey] = item

        item.clicked.connect(self._onClicked)
        if onClick:
            item.clicked.connect(onClick)
        if isSelected:
            self.setCurrentWidget(routeKey)
        if toolTip:
            setToolTipInfo(item, toolTip, 1500, ToolTipPosition.TOP)

    def addWidget(self, widget: QWidget) -> None:
        self.insertWidget(-1, widget)

    def insertWidget(self, index: int, widget: QWidget) -> None:
        self._widgetLayout.insertWidget(index, widget)

    def removeItem(self, routeKey: str) -> Union[None, SlidingWidget]:
        if routeKey not in self._items:
            return None
        widget = self._items.pop(routeKey)
        self._widgetLayout.removeWidget(widget)
        widget.clicked.disconnect()
        widget.setParent(None)
        if self._items and self.__currentItem is widget:
            item = self._items[next(iter(self._items))]
            self.__currentItem = item
            self._onClicked(item)
        return widget

    def currentItem(self) -> Union[SlidingWidget, None]:
        return self.__currentItem

    def item(self, routeKey: str) -> SlidingWidget:
        if routeKey not in self._items:
            raise RouteKeyError(f"`{routeKey}` is illegal")
        return self._items[routeKey]

    def allItem(self) -> List[SlidingWidget]:
        return list(self._items.values())

    def eventFilter(self, obj, event) -> bool:
        if event.type() in [QEvent.Resize, QEvent.WindowStateChange] and self.__currentItem:
            self._adjustSlideLinePos()
        return super().eventFilter(obj, event)


class SlidingToolNavigationBar(SlidingNavigationBar):

    def __init__(self, parent) -> None:
        super().__init__(parent)

    def setIconSize(self, size: int) -> None:
        for item in self.allItem():
            item.setIconSize(size)

    def addItem(
            self,
            routeKey: str,
            icon: FluentIcon,
            onClick=None,
            isSelected=False,
            toolTip: str = None
    ):
        self.insertItem(-1, routeKey, icon, onClick, isSelected, toolTip)

    def insertItem(
            self,
            index: int,
            routeKey: str,
            icon: FluentIcon,
            onClick=None,
            isSelected=False,
            toolTip: str = None
    ):
        if routeKey in self._items:
            raise RouteKeyError('routeKey Are Not Unique')
        item = SlidingWidget('', icon, isSelected, self._widget)
        item.setProperty("routeKey", routeKey)
        self._widgetLayout.insertWidget(index, item)
        self._items[routeKey] = item

        item.clicked.connect(self._onClicked)
        if onClick:
            item.clicked.connect(onClick)
        if isSelected:
            self.setCurrentWidget(routeKey)
        if toolTip:
            setToolTipInfo(item, toolTip, 1500, ToolTipPosition.TOP)