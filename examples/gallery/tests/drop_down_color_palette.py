# coding:utf-8
import sys
from typing import Union

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QAbstractButton, QLayout
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, QPoint, QRectF, QEvent, Signal, QSize, QRect

from PySide6FluentUI import SplitWidget, TransparentToolButton, FluentIcon, toggleTheme, \
    TransparentPushButton, themeColor, HorizontalSeparator, BodyLabel, \
    isDarkTheme, getFont

from app.common.config import update
from popup_view import PopupView


class StandardItem(QAbstractButton):

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

        margin = self.height() / 5
        rect = QRectF(margin, margin, 24, 24)
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


class DropDownColorPalette(QWidget):
    colorChanged = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        parent.installEventFilter(self)
        from PySide6FluentUI import ColorDialog
        self.__currentColor: QColor = None
        self.__lastButton: ColorItem = None
        self.widgetLayout: QHBoxLayout = QHBoxLayout(self)
        self.colorPaletteView: PopupView = PopupView(self)
        self.colorPaletteView.setFixedSize(346, 400)
        self.__initColorPaletteView()

        self.colorItem: StandardItem = StandardItem(self.defaultColor(), self)
        self.dropDownButton: TransparentToolButton = TransparentToolButton(FluentIcon.CHEVRON_DOWN_MED, self)
        self.colorDialog: ColorDialog = ColorDialog(self.defaultColor(), "选择颜色", self.window())

        self.colorDialog.hide()
        self.colorItem.setFixedSize(26, 26)
        self.dropDownButton.setIconSize(QSize(14, 14))
        self.widgetLayout.setContentsMargins(6, 6, 6, 6)
        self.widgetLayout.setSizeConstraint(QLayout.SetFixedSize)

        self.widgetLayout.addWidget(self.colorItem)
        self.widgetLayout.addWidget(self.dropDownButton)
        self.connectSignalSlot()

        # self.setMouseTracking(True)
    def __initColorPaletteView(self):
        self.__initButtonGroup()

        # init default color item
        self.defaultColorItem: DefaultColorPaletteItem = DefaultColorPaletteItem(themeColor(), "默认颜色", self.colorPaletteView)
        self.defaultColorItem.setFixedHeight(42)
        self.colorPaletteView.viewLayout.addWidget(self.defaultColorItem)
        self.colorPaletteView.viewLayout.addWidget(HorizontalSeparator(self))

        # init theme color
        self.themeColorLabel: BodyLabel = BodyLabel("   主题色", self.colorPaletteView)
        self.colorPaletteView.viewLayout.addWidget(self.themeColorLabel)
        self.colorPaletteView.viewLayout.addSpacing(8)

        hBoxLayout = QHBoxLayout()
        hBoxLayout.setSpacing(1)
        hBoxLayout.setContentsMargins(5, 0, 5, 0)
        colors = ["#1E90FF", "#FF4500", "#9ACD32", "#8A2BE2", "#FF1493", "#00CED1", "#00FF95", "#DC143C", "#8A8A8A", "#FF8C00"]
        for i in range(10):
            color = colors[i]
            vBoxLayout = QVBoxLayout()
            vBoxLayout.setSpacing(4)
            item = ColorItem(colors[i], self)
            vBoxLayout.addWidget(item)

            self.colorButtonGroup.addButton(item)
            for j in range(5):
                color = QColor(color)
                color.setAlpha(255 / (5 - j))
                item = ColorItem(color, self)
                vBoxLayout.addWidget(item)
                self.colorButtonGroup.addButton(item)
            hBoxLayout.addLayout(vBoxLayout)

        self.colorPaletteView.viewLayout.addLayout(hBoxLayout)
        self.colorPaletteView.viewLayout.addSpacing(10)
        self.colorPaletteView.viewLayout.addWidget(HorizontalSeparator(self))

        # init standard color
        self.standardColorLabel: BodyLabel = BodyLabel("   标准颜色", self.colorPaletteView)
        self.colorPaletteView.viewLayout.addWidget(self.standardColorLabel, 0, Qt.AlignLeft | Qt.AlignVCenter)
        self.colorPaletteView.viewLayout.addSpacing(8)

        hBoxLayout = QHBoxLayout()
        hBoxLayout.setSpacing(0)
        hBoxLayout.setContentsMargins(4, 0, 5, 0)
        colors = ["#FF0000", "#0000FF", "#008000", "#FFFF00", "#00FFFF", "#FF00FF", "#000000", "#FFFFFF", "#FFA500", "#800080"]

        for color in colors:
            item = ColorItem(color, self)
            hBoxLayout.addWidget(item)
            self.colorButtonGroup.addButton(item)
        self.colorPaletteView.viewLayout.addLayout(hBoxLayout)

        self.colorPaletteView.viewLayout.addSpacing(10)
        self.colorPaletteView.viewLayout.addWidget(HorizontalSeparator(self))

        self.customColorButton: TransparentPushButton = TransparentPushButton(FluentIcon.PALETTE, "更多颜色")
        self.customColorButton.setFixedHeight(42)
        self.colorPaletteView.viewLayout.addWidget(self.customColorButton)

    def __initButtonGroup(self):
        self.colorButtonGroup: QButtonGroup = QButtonGroup(self)
        self.colorButtonGroup.setExclusive(True)
        self.__defaultButton: ColorItem = ColorItem('')
        self.colorButtonGroup.addButton(self.__defaultButton)
        self.colorButtonGroup.setId(self.__defaultButton, 0)

    def __updateSelectedColor(self, color: QColor):
        self.colorChanged.emit(color)
        self.__currentColor = color
        self.colorItem.setColor(color)
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
            self.colorChanged.emit(color)
            self.__currentColor = color

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
        self.colorItem.setColor(color)
        self.__currentColor = color

    def exec(self):
        positon = self.mapToGlobal(self.dropDownButton.geometry().center())
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

    def currentColor(self) -> QColor:
        return self.__currentColor

    def eventFilter(self, watched, event):
        if watched != self and event.type() in [QEvent.MouseButtonPress]:
            self.colorPaletteView.hide()
        return super().eventFilter(watched, event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.exec()
        super().mouseReleaseEvent(event)

    def connectSignalSlot(self):
        self.defaultColorItem.clicked.connect(self.__onClickedDefaultColorItem)
        self.colorButtonGroup.buttonClicked.connect(self.__onClicked)
        self.customColorButton.clicked.connect(self._showColorDialog)
        self.dropDownButton.clicked.connect(self.exec)
        self.colorDialog.colorChanged.connect(self.__onClickedCustomColorButton)
        self.colorChanged.connect(self.colorItem.setColor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        c = 255 if isDarkTheme() else 0
        painter.setPen(QColor(c, c, c, 32))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 8, 8)


class Window(SplitWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.box: QVBoxLayout = QVBoxLayout(self)
        self.toggleButton: TransparentToolButton = TransparentToolButton(FluentIcon.BROOM, self)
        self.colorPalette: DropDownColorPalette = DropDownColorPalette(self)

        self.toggleButton.setFixedSize(46, 32)
        self.titleBar.hBoxLayout.insertWidget(4, self.toggleButton)
        self.toggleButton.clicked.connect(lambda: {
            toggleTheme(), update()
        })

        self.box.setContentsMargins(11, 38, 11, 11)
        self.box.addWidget(self.colorPalette, 0, Qt.AlignCenter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
