# coding:utf-8
from typing import Union, List

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QAbstractButton, QLayout
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, QPoint, QRectF, Signal, QSize, QRect

from .popup_view import PopupView
from .button import TransparentToolButton, TransparentPushButton
from .separator import HorizontalSeparator
from .label import BodyLabel
from ...common.style_sheet import isDarkTheme, themeColor
from ...common.icon import FluentIcon
from ...common.font import getFont


class BaseItem(QAbstractButton):

    def __init__(self, color: Union[str, QColor], parent=None):
        super().__init__(parent)
        self.__color = QColor(color) if isinstance(color, str) else color

    def setColor(self, color: Union[str, QColor]) -> None:
        if isinstance(color, str):
            color = QColor(color)
        if self.__color == color:
            return
        self.__color = color
        self.update()

    def color(self) -> QColor:
        return self.__color

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color())
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class DefaultColorPaletteItem(BaseItem):

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
        painter.setBrush(self.color())

        margin = self.height() / 5
        rect = QRectF(margin, margin, 24, 24)
        isDark = isDarkTheme()

        painter.drawRoundedRect(rect, 4, 4)

        rect = self.rect()
        if self.isHover:
            c = 255 if isDark else 0
            painter.setBrush(QColor(c, c, c, 32))
            painter.drawRoundedRect(rect, 4, 4)

        # draw text
        if self.text():
            painter.setFont(getFont())
            c = 255 if isDark else 0
            painter.setPen(QColor(c, c, c))
            painter.drawText(rect.adjusted(40, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, self.text())


class ColorItem(DefaultColorPaletteItem):

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


class ColorView(QWidget):
    colorChanged = Signal(QColor)

    def __init__(self, defaultColor=QColor(255, 255, 255), parent=None):
        super().__init__(parent)
        self.__currentColor: QColor = defaultColor
        self.colorItem: BaseItem = BaseItem(defaultColor, self)
        self.widgetLayout: QHBoxLayout = QHBoxLayout(self)
        self.pickerColorButton: TransparentToolButton = TransparentToolButton(self)

        self.colorItem.setFixedSize(26, 26)
        self.__initLayout()

    def __initLayout(self):
        self.widgetLayout.setContentsMargins(5, 5, 5, 5)
        self.widgetLayout.setSpacing(2)
        self.widgetLayout.setSizeConstraint(QLayout.SetFixedSize)

        self.widgetLayout.addWidget(self.colorItem)
        self.widgetLayout.addWidget(self.pickerColorButton)

    def setDefaultColor(self, color: Union[str, QColor]):
        self.colorItem.setColor(color)

    def setCurrentColor(self, color: Union[str, QColor]):
        self.__currentColor = color

    def currentColor(self) -> QColor:
        return self.__currentColor

    def connectSignalSlot(self): ...

    def exec(self): ...

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        c = 255 if isDarkTheme() else 0
        painter.setPen(QColor(c, c, c, 32))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)


class DropDownColorPalette(ColorView):

    def __init__(self, parent=None, colors=[
        QColor("#FFFFFF"), QColor("#FF0000"), QColor("#00BFFF"), QColor("#00FF7F"), QColor("#FF00FF"),
        QColor("#8A2BE2"), QColor("#A5A5A5"), QColor("#FFC000"), QColor("#EE9A00"), QColor("#70AD47")]):
        super().__init__(parent=parent)
        from ..dialog_box import ColorDialog
        self.__lastButton: ColorItem = None
        self.__colors: List[QColor] = colors
        self.colorPaletteView: PopupView = PopupView(self)

        self.colorPaletteView.setFixedSize(346, 414)
        self.pickerColorButton.setIcon(FluentIcon.CHEVRON_DOWN_MED)
        self.pickerColorButton.setIconSize(QSize(12, 12))
        self.__initColorPaletteView()

        self.colorDialog: ColorDialog = ColorDialog(self.defaultColor(), "选择颜色", self.window())
        self.colorDialog.hide()
        self.connectSignalSlot()

    def __initColorPaletteView(self):
        self.__initButtonGroup()

        # init default color item
        self.defaultColorItem: DefaultColorPaletteItem = DefaultColorPaletteItem(themeColor(), "默认颜色", self.colorPaletteView)
        self.defaultColorItem.setFixedHeight(40)
        self.colorPaletteView.viewLayout.addWidget(self.defaultColorItem)
        self.colorPaletteView.viewLayout.addWidget(HorizontalSeparator(self))

        # init theme color
        self.themeColorLabel: BodyLabel = BodyLabel("   主题色", self.colorPaletteView)
        self.colorPaletteView.viewLayout.addWidget(self.themeColorLabel)
        self.colorPaletteView.viewLayout.addSpacing(8)
        self.__buildThemeColor()

        # init standard color
        self.standardColorLabel: BodyLabel = BodyLabel("   标准颜色", self.colorPaletteView)
        self.colorPaletteView.viewLayout.addWidget(self.standardColorLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.colorPaletteView.viewLayout.addSpacing(8)
        self.__buildBaseColor()

        self.customColorButton: TransparentPushButton = TransparentPushButton(FluentIcon.PALETTE, "更多颜色")
        self.customColorButton.setFixedHeight(40)
        self.colorPaletteView.viewLayout.addWidget(self.customColorButton)

    def __buildThemeColor(self):
        self.themeColorLayout: QHBoxLayout = QHBoxLayout()
        self.themeColorLayout.setSpacing(1)
        self.themeColorLayout.setContentsMargins(5, 0, 5, 0)

        for color in self.__colors:
            vBoxLayout = QVBoxLayout()
            vBoxLayout.setSpacing(4)
            item = ColorItem(color, self)
            vBoxLayout.addWidget(item)
            vBoxLayout.addSpacing(5)

            self.colorButtonGroup.addButton(item)
            for _c_ in self.colorScale(color):
                item = ColorItem(_c_, self)
                vBoxLayout.addWidget(item)
                self.colorButtonGroup.addButton(item)
            self.themeColorLayout.addLayout(vBoxLayout)

        self.colorPaletteView.viewLayout.addLayout(self.themeColorLayout)
        self.colorPaletteView.viewLayout.addSpacing(10)
        self.colorPaletteView.viewLayout.addWidget(HorizontalSeparator(self))

    def __buildBaseColor(self):
        hBoxLayout = QHBoxLayout()
        hBoxLayout.setSpacing(0)
        hBoxLayout.setContentsMargins(4, 0, 5, 0)

        for _h in [36 * _ for _ in range(10)]:
            item = ColorItem(QColor.fromHsv(_h, 255, 255), self)
            hBoxLayout.addWidget(item)
            self.colorButtonGroup.addButton(item)
        self.colorPaletteView.viewLayout.addLayout(hBoxLayout)

        self.colorPaletteView.viewLayout.addSpacing(10)
        self.colorPaletteView.viewLayout.addWidget(HorizontalSeparator(self))

    def __initButtonGroup(self):
        self.colorButtonGroup: QButtonGroup = QButtonGroup(self)
        self.colorButtonGroup.setExclusive(True)
        self.__defaultButton: ColorItem = ColorItem('')
        self.colorButtonGroup.addButton(self.__defaultButton)
        self.colorButtonGroup.setId(self.__defaultButton, 0)

    def __updateSelectedColor(self, color: QColor):
        self.setCurrentColor(color)
        self.colorItem.setColor(color)
        self.colorChanged.emit(color)
        self.__lastButton = None
        self.colorButtonGroup.button(0).setChecked(True)

    def __onClickedDefaultColorItem(self):
        self.__updateSelectedColor(self.defaultColor())
        self.colorPaletteView.hide()

    def __onClickedCustomColorButton(self, color: QColor):
        self.__updateSelectedColor(color)

    def __onClicked(self, item):
        color = self.updateItem(item)
        if color:
            self.setCurrentColor(color)
            self.colorChanged.emit(color)

    def colorScale(self, base: QColor, steps=5):
        colors = []
        for i in range(1, steps + 1):
            factor = 100 + (i * 16)
            colors.append(base.darker(factor))
        return colors

    def updateItem(self, button: ColorItem) -> Union[QColor, bool]:
        if self.__lastButton and button != self.__lastButton:
            self.__lastButton.isHover = False
            self.__lastButton.setChecked(False)
            self.__lastButton.update()
        self.colorPaletteView.hide()
        try:
            color = self.__lastButton.color()
        except AttributeError:
            color = QColor()
        self.__lastButton = button
        return button.color() if button.color() != color else False

    def setDefaultColor(self, color: Union[str, QColor]) -> None:
        self.defaultColorItem.setColor(color)
        super().setDefaultColor(color)
        self.setCurrentColor(color)

    def exec(self):
        positon = self.mapToGlobal(self.pickerColorButton.geometry().center())
        x = positon.x() + self.width() // 2
        y = int(positon.y() - self.colorPaletteView.height() // 2.2)
        startPos, endPos = QPoint(x - 24, y), QPoint(x, y)

        rect = QRect(endPos, self.colorPaletteView.size())
        screen = QApplication.screenAt(endPos)
        if not screen:
            screen = QApplication.primaryScreen()
        available = screen.availableGeometry()
        if not available.contains(rect):
            right = max(0, rect.right() - available.right())
            bottom = max(0, rect.bottom() - available.bottom())
            startPos -= QPoint(right, bottom)
            endPos -= QPoint(right, bottom)

        self.colorPaletteView.exec(startPos, endPos)

    def defaultColor(self) -> QColor:
        return self.defaultColorItem.color()

    def _showColorDialog(self):
        self.colorPaletteView.hide()
        self.colorDialog.exec()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.exec()
        super().mouseReleaseEvent(event)

    def connectSignalSlot(self):
        self.defaultColorItem.clicked.connect(self.__onClickedDefaultColorItem)
        self.colorButtonGroup.buttonClicked.connect(self.__onClicked)
        self.customColorButton.clicked.connect(self._showColorDialog)
        self.pickerColorButton.clicked.connect(self.exec)
        self.colorDialog.colorChanged.connect(self.__onClickedCustomColorButton)
        self.colorChanged.connect(self.colorItem.setColor)