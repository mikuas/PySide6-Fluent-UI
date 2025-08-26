# coding:utf-8
from typing import Union

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QButtonGroup
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, QSize, Signal, QPoint, QRectF

from ...common.font import getFont
from ...common.config import isDarkTheme
from ...common.icon import FluentIcon
from ...common.color import themeColor
from .button import TransparentToolButton, TransparentPushButton
from .separator import HorizontalSeparator
from .menu import RoundMenu, MenuAnimationType
from .label import BodyLabel


class StandardItem(QPushButton):

    def __init__(self, color: Union[str, QColor], parent=None):
        super().__init__(parent)
        self.setColor(color)

    def setColor(self, color: Union[str, QColor]) -> None:
        if isinstance(color, str):
            color = QColor(color)
        self._color = color
        self.update()

    def color(self) -> QColor:
        return self._color

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color())
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class DefaultColorPaletteItem(StandardItem):
    
    def __init__(self, color: Union[str, QColor], text: str, parent: QWidget = None):
        super().__init__(color, parent)
        self._text: str = text
        self.isHover: bool = False
        self.setFixedHeight(35)
    
    def setText(self, text: str):
        self._text = text
        self.update()

    def text(self):
        return self._text

    def enterEvent(self, event):
        self.isHover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.isHover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color)
        
        rect = QRectF(6.36, 6.36, 24, 24)
        isDark = isDarkTheme()
        
        painter.drawRoundedRect(rect, 4, 4)

        rect = self.rect()
        if self.isHover:
            c = 255 if isDark else 0
            painter.setBrush(QColor(c, c, c, 32))
            painter.drawRoundedRect(rect, 4, 4)

        if self.text():
            painter.setFont(getFont())
            c = 255 if isDark else 0
            painter.setPen(QColor(c, c, c))
            painter.drawText(rect.adjusted(40, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, self.text())


class ColorPaletteItem(DefaultColorPaletteItem):

    def __init__(self, color: Union[str, QColor], parent=None):
        super().__init__(color, "", parent)
        self.setMouseTracking(True)
        self.setCheckable(True)
        self.setFixedSize(28, 28)
        
    def setChecked(self, isChecked: bool):
        super().setChecked(isChecked)
        self.update()
        
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.isHover:
            self.setChecked(not self.isChecked())
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = QRectF(self.rect())
        if self.isChecked():
            self._drawBorder(painter, rect)
            rect.adjust(3.1, 3.1, -3.1, -3.1)
            self._drawBackground(painter, rect)
            return
        elif self.isHover:
            self._drawBorder(painter, rect)
            self._drawBackground(painter, rect.adjusted(2.1, 2.1, -2.1, -2.1))
        else:
            self._drawBackground(painter, rect)

    def _drawBorder(self, painter: QPainter, rect: QRectF) -> None:
        c = 255 if isDarkTheme() else 0
        painter.setPen(QColor(c, c, c))
        painter.drawRoundedRect(rect.adjusted(1.1, 1.1, -1.1, -1.1), 6, 6)

    def _drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color())
        painter.drawRoundedRect(rect, 3.7, 3.7)


class ColorPalette(RoundMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.colorButtonGroup: QButtonGroup = QButtonGroup(self)
        self.colorButtonGroup.setExclusive(True)
        self.__defaultButton: ColorPaletteItem = ColorPaletteItem('')
        self.colorButtonGroup.addButton(self.__defaultButton)
        self.colorButtonGroup.setId(self.__defaultButton, 0)
        
        self._lastButton: ColorPaletteItem = None
        self.setMouseTracking(True)
        self.__initPaletteWidget()
        self.__initDefaultColor()
        self.__initThemeColor()
        self.__initStandardColor()

        self.moreColorButton: TransparentPushButton = TransparentPushButton(FluentIcon.PALETTE, "更多颜色")
        self.moreColorButton.setFixedWidth(320)
        
        self._widgetLayout.addWidget(self.moreColorButton)

    def __initPaletteWidget(self):
        self.view.setFixedSize(350, 390)
        self.setFixedSize(350, 390)
        self.setItemHeight(390)
        self.view.setStyleSheet("padding: 0px 0px 0px 0px; border-radius: 6px;")
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._widget: QWidget = QWidget()
        self._widget.setFixedSize(350, 390)
        self.addWidget(self._widget, False)

        self._widgetLayout: QVBoxLayout = QVBoxLayout(self._widget)
        self._widgetLayout.setAlignment(Qt.AlignTop)
        self._widgetLayout.setContentsMargins(0, 0, 0, 0)
        self._widgetLayout.setSpacing(4)

    def __initDefaultColor(self):
        self.defaultColorItem: DefaultColorPaletteItem = DefaultColorPaletteItem(themeColor(), "默认颜色", self)
        self.defaultColorItem.setFixedWidth(320)
        self._widgetLayout.addWidget(self.defaultColorItem)
        self._widgetLayout.addWidget(self.__createHorizontalSeparator())

    def __initThemeColor(self):
        self.themeColorLabel: BodyLabel = BodyLabel("主题色", self._widget)
        self._widgetLayout.addWidget(self.themeColorLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)

        hBoxLayout = QHBoxLayout()
        hBoxLayout.setSpacing(4)
        colors = ["#1E90FF", "#FF4500", "#9ACD32", "#8A2BE2", "#FF1493", "#00CED1", "#00FF95", "#DC143C", "#8A8A8A", "#FF8C00"]
        for i in range(10):
            color = colors[i]
            vBoxLayout = QVBoxLayout()
            vBoxLayout.setSpacing(4)
            item = ColorPaletteItem(colors[i], self)
            vBoxLayout.addWidget(item)
            
            self.colorButtonGroup.addButton(item)
            vBoxLayout.addSpacing(10)
            for j in range(5):
                color = QColor(color)
                color.setAlpha(255 / (5 - j))
                item = ColorPaletteItem(color, self)
                vBoxLayout.addWidget(item)
                self.colorButtonGroup.addButton(item)
            hBoxLayout.addLayout(vBoxLayout)
        
        self._widgetLayout.addLayout(hBoxLayout)

        self._widgetLayout.addSpacing(10)
        self._widgetLayout.addWidget(self.__createHorizontalSeparator())

    def __initStandardColor(self):
        self.standardColorLabel: BodyLabel = BodyLabel("标准颜色", self)
        self._widgetLayout.addWidget(self.standardColorLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        box = QHBoxLayout()
        colors = ["#FF0000", "#0000FF", "#008000", "#FFFF00", "#00FFFF", "#FF00FF", "#000000", "#FFFFFF", "#FFA500", "#800080"]

        for color in colors:
            item = ColorPaletteItem(color, self)
            box.addWidget(item)
            self.colorButtonGroup.addButton(item)
        self._widgetLayout.addLayout(box)

        self._widgetLayout.addSpacing(10)
        self._widgetLayout.addWidget(self.__createHorizontalSeparator())

    def __createHorizontalSeparator(self):
        separator = HorizontalSeparator(self)
        separator.setFixedWidth(320)
        return separator

    def updateItem(self, button: ColorPaletteItem) -> Union[QColor, bool]:
        if self._lastButton and button != self._lastButton:
            self._lastButton.isHover = False
            self._lastButton.setChecked(False)
            self._lastButton.update()
        self.hide()
        try:
            color = self._lastButton.color()
        except AttributeError:
            color = QColor()
        self._lastButton = button
        return button.color() if button.color() != color else False

    def setDefaultColor(self, color: Union[str, QColor]) -> None:
        self.defaultColorItem.setColor(color)

    def defaultColor(self) -> QColor:
        return self.defaultColorItem.color()

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        super().exec(pos, ani, aniType)
        self.adjustSize()


class DropDownColorPalette(QWidget):

    colorChanged: Signal = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        from ..dialog_box import ColorDialog
        self.setMinimumSize(62, 40)
        self.__currentColor: QColor = None
        
        self.widgetLayout: QHBoxLayout = QHBoxLayout(self)
        self.colorPalette: ColorPalette = ColorPalette(self)
        self.item: StandardItem = StandardItem(self.colorPalette.defaultColor(), self)
        self.dropDownButton: TransparentToolButton = TransparentToolButton(FluentIcon.CHEVRON_DOWN_MED, self)
        self.colorDialog: ColorDialog = ColorDialog(self.colorPalette.defaultColor(), "选择颜色", self.window(), True)

        self.colorDialog.hide()
        self.item.setFixedSize(28, 28)
        self.dropDownButton.setIconSize(QSize(12, 12))
        self.widgetLayout.setContentsMargins(5, 3, 5, 3)

        self.widgetLayout.addWidget(self.item)
        self.widgetLayout.addWidget(self.dropDownButton)
        self.__initSignalSlot()

    def setDefaultColor(self, color: Union[str, QColor]) -> None:
        self.colorPalette.setDefaultColor(color)
        self.item.setColor(color)
        self.__currentColor = color
    
    def defaultColor(self) -> QColor:
        return self.colorPalette.defaultColor()

    def currentColor(self) -> QColor:
        return self.__currentColor
    
    def __updateSelectedColor(self, color: QColor):
        self.colorChanged.emit(color)
        self.__currentColor = color
        self.item.setColor(color)
        self.colorPalette._lastButton = None
        self.colorPalette.colorButtonGroup.button(0).setChecked(True)
    
    def __onClickedDefaultColorItem(self):
        self.__updateSelectedColor(self.colorPalette.defaultColor())
        self.colorPalette.hide()
    
    def __onClickedMoreColorItem(self, color: QColor):
        self.__updateSelectedColor(color)
        
    def __point(self) -> QPoint:
        return self.mapToGlobal(QPoint(-(self.colorPalette.width() / 2) + (self.width() / 1.5) , self.height()))

    def __showColorPalette(self):
        self.colorPalette.exec(self.__point())

    def __showColorDialog(self):
        self.colorPalette.hide()
        self.colorDialog.exec()

    def __initSignalSlot(self):
        self.colorPalette.defaultColorItem.clicked.connect(self.__onClickedDefaultColorItem)
        self.colorPalette.colorButtonGroup.buttonClicked.connect(self.__onClickItem)
        self.colorPalette.moreColorButton.clicked.connect(self.__showColorDialog)
        self.dropDownButton.clicked.connect(self.__showColorPalette)
        self.colorDialog.colorChanged.connect(self.__onClickedMoreColorItem)
        self.colorChanged.connect(self.item.setColor)

    def __onClickItem(self, item):
        color = self.colorPalette.updateItem(item)
        if color:
            self.colorChanged.emit(color)
            self.__currentColor = color

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.colorPalette.exec(self.__point())
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        c = 255 if isDarkTheme() else 0
        painter.setPen(QColor(c, c, c, 32))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)