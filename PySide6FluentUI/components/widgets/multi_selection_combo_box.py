# coding:utf-8
from typing import List

from PySide6.QtWidgets import QWidget, QHBoxLayout, QStyledItemDelegate, QStyle, QListWidget, QListWidgetItem
from PySide6.QtGui import QColor, QPainter, QFontMetrics
from PySide6.QtCore import Qt, QSize, Signal

from .combo_box import ComboBoxMenu
from .check_box import CheckBox
from .scroll_area import SingleDirectionScrollArea, SmoothScrollDelegate
from .button import TransparentToolButton
from .tool_tip import setToolTipInfo
from ...common.config import isDarkTheme
from ...common.icon import FluentIcon


class MultiSelectionItemCheckBox(CheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, e):
        e.ignore()


class MultiSelectionItemDelegate(QStyledItemDelegate):

    def __init__(self, parent: QListWidget):
        super().__init__(parent)
        self._listWidget: QListWidget = parent

    def paint(self, painter, option, index):
        painter.save()

        rect = option.rect.adjusted(1, 1, -1, -1)
        isCheck = self._listWidget.item(index.row()).isChecked()
        isDark = isDarkTheme()
        if isCheck:
            color = "#202020" if isDark else "#f0f0f0"
        else:
            if option.state & QStyle.State_MouseOver:
                color = "#202020" if isDark else "#f0f0f0"
            else:
                color = "#2b2b2b" if isDark else "#ffffff"
        painter.setRenderHint(QPainter.Antialiasing | QPainter.TextAntialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(color))
        painter.drawRoundedRect(rect, 6, 6)
        painter.restore()


class MultiSelectionListItem(QListWidgetItem):

    def __init__(self, text: str, parent: QWidget = None):
        super().__init__(text, parent)
        self.widget: QWidget = QWidget(parent)
        self.layout: QHBoxLayout = QHBoxLayout(self.widget)
        self.checkBox: MultiSelectionItemCheckBox = MultiSelectionItemCheckBox(text, self.widget)
        self.layout.addWidget(self.checkBox)
        self.layout.setContentsMargins(10, 0, 0, 0)

    def setChecked(self, isChecked) -> None:
        self.checkBox.setChecked(isChecked)

    def isChecked(self) -> bool:
        return self.checkBox.isChecked()


class MultiSelectionListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.itemDelegate: MultiSelectionItemDelegate = MultiSelectionItemDelegate(self)
        self.scrollDelegate: SmoothScrollDelegate = SmoothScrollDelegate(self)
        self.setItemDelegate(self.itemDelegate)
        self.setMouseTracking(True)
        self.itemClicked.connect(self.updateCheckedState)

    def updateCheckedState(self, item: MultiSelectionListItem) -> None:
        item.setChecked(not item.isChecked())

    def item(self, row) -> MultiSelectionListItem:
        return super().item(row)

    def takeItem(self, row) -> MultiSelectionListItem:
        return super().takeItem(row)

    def addItem(self, text: str) -> None:
        item = MultiSelectionListItem(text, self)
        item.setSizeHint(QSize(0, 40))
        super().addItem(item)
        self.setItemWidget(item, item.widget)

    def addItems(self, labels) -> None:
        items = []
        for item in labels:
            self.addItem(item)
            items.append(item)


class MultiSelectionItem(QWidget):

    removeSignal: Signal = Signal(QWidget)

    def __init__(self, text: str, parent: QWidget = None):
        super().__init__(parent)
        self.setFixedHeight(26)
        self._box: QHBoxLayout = QHBoxLayout(self)
        self._text: str = text
        self.isHover: bool = False
        self.isPress: bool = False
        self.setContentsMargins(0, 0, 0, 0)
        self._box.setContentsMargins(5, 0, 5, 0)

        self._removeButton: TransparentToolButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self._removeButton.setIconSize(QSize(10, 10))
        self._removeButton.setCursor(Qt.PointingHandCursor)
        self._removeButton.clicked.connect(lambda: self.removeSignal.emit(self))

        setToolTipInfo(self._removeButton, "删除", 1000)
        self._box.addWidget(self._removeButton, alignment=Qt.AlignRight | Qt.AlignVCenter)
        self._box.setContentsMargins(0, 0, 5, 0)

    def text(self) -> str:
        return self._text

    def sizeHint(self):
        metrics = QFontMetrics(self.font())
        width = metrics.horizontalAdvance(self._text)
        return QSize(width + self._removeButton.width() * 2, self.height())

    def minimumSizeHint(self):
        return self.sizeHint()

    def enterEvent(self, event):
        self.isHover = True
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        self.isHover = False
        self.isPress = False
        super().leaveEvent(event)
        self.update()

    def mousePressEvent(self, event):
        self.isPress = True
        super().mousePressEvent(event)
        self.update()

    def mouseReleaseEvent(self, event):
        self.isPress = False
        event.accept()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        isDark = isDarkTheme()
        color = QColor("#2b2b2b" if isDark else "#EAEAEA")
        if self.isHover:
            color.setAlpha(186)
        if self.isPress:
            color.setAlpha(214)
        painter.setBrush(color)
        painter.drawRoundedRect(self.rect(), 6, 6)

        painter.setPen("#ffffff" if isDark else "#000000")
        painter.drawText(
            self.rect().adjusted(0, 0, -self._removeButton.width(), 0), Qt.AlignCenter, self.text()
        )


class MultiSelectionComboBox(QWidget):

    selectedChange: Signal = Signal(list)   # return type: List[MultiSelectionItem]

    def __init__(self, parent: QWidget = None, placeholder: str = None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setContentsMargins(0, 0, 0, 0)
        self.__initScrollWidget()
        self._texts: List[str] = []
        self._items: List[MultiSelectionItem] = []
        self._displayItems: List[MultiSelectionItem] = []
        self.__hasItem: bool = False
        self.__enableClearButton: bool = False
        self._placeholder: str = placeholder
        self._hBoxLayout: QHBoxLayout = QHBoxLayout(self)
        self._widgetLayout: QHBoxLayout = QHBoxLayout(self._widget)
        self._hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.__initMultiSelectionListWidget()
        self.__initMenu()
        self.__initWidget()
        self._connectSignalSlot()

    def __initScrollWidget(self):
        self._scrollArea: SingleDirectionScrollArea = SingleDirectionScrollArea(self, Qt.Horizontal)
        self._widget: QWidget = QWidget(self)
        self._scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scrollArea.setWidgetResizable(True)
        self._scrollArea.setWidget(self._widget)
        self._scrollArea.enableTransparentBackground()
    
    def __initLayout(self):
        self._widgetLayout.setContentsMargins(5, 0, 5, 0)
        self._hBoxLayout.setContentsMargins(5, 0, 5, 0)
        self._hBoxLayout.addWidget(self._scrollArea, 1)
        self._hBoxLayout.addWidget(self.clearButton, 0, Qt.AlignCenter | Qt.AlignRight)
        self._hBoxLayout.addWidget(self.dropButton, 0, Qt.AlignCenter | Qt.AlignRight)

    def __initWidget(self):
        self.clearButton: TransparentToolButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self.dropButton: TransparentToolButton = TransparentToolButton(FluentIcon.CHEVRON_DOWN_MED, self)

        self.clearButton.setFixedSize(32, 32)
        self.dropButton.setFixedSize(32, 24)
        self.clearButton.setIconSize(QSize(8, 8))
        self.dropButton.setIconSize(QSize(8, 8))
        self.clearButton.setVisible(False)
        self.clearButton.setCursor(Qt.PointingHandCursor)

        self.__initLayout()
        setToolTipInfo(self.clearButton, "清除所有选中项", 1000)
    
    def __initMenu(self):
        self._menu: ComboBoxMenu = ComboBoxMenu(self)
        self._menu.view.setStyleSheet("padding: 0px 0px 0px 0px; border-radius: 6px;")
        self._menu.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._menu.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._menu.addWidget(self.multiSelectionListWidget, False)
        self._menu.setItemHeight(41)

    def __initMultiSelectionListWidget(self):
        self.multiSelectionListWidget: MultiSelectionListWidget = MultiSelectionListWidget(self)
        self.multiSelectionListWidget.setStyleSheet("background: transparent;")
        self.multiSelectionListWidget.setFixedHeight(256)
        self.multiSelectionListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.multiSelectionListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def __updateHasWidget(self, item) -> None:
        flag = len(item) > 0
        if flag and self.__hasItem:
            return
        if self.__enableClearButton:
            self.clearButton.setVisible(flag)
        self.__hasItem = flag
        self.update()

    def _connectSignalSlot(self) -> None:
        self.clearButton.clicked.connect(self.clearAllSelected)
        self.dropButton.clicked.connect(self._showMenu)
        self.multiSelectionListWidget.itemClicked.connect(self._itemOnClicked)
        self.selectedChange.connect(self.__updateHasWidget)

    def _showMenu(self) -> None:
        self._menu.exec(self.mapToGlobal(self.rect().bottomLeft()))

    def _itemOnClicked(self, item: MultiSelectionListItem) -> None:
        isChecked = item.isChecked()
        item.setChecked(isChecked)
        self.updateCheckedState(self._items[self.multiSelectionListWidget.row(item)], isChecked)

    def updateCheckedState(self, item: MultiSelectionItem, isChecked=False) -> None:
        self.multiSelectionListWidget.item(self._items.index(item)).setChecked(isChecked)
        if isChecked:
            self._widgetLayout.addWidget(item)
            self._displayItems.append(item)
            item.show()
        else:
            item.hide()
            self._widgetLayout.removeWidget(item)
            self._displayItems.remove(item)
        self.selectedChange.emit(self._displayItems)

    def setMaxVisibleItems(self, num: int) -> None:
        self._menu.setMaxVisibleItems(num)

    def setPlaceholderText(self, text: str) -> None:
        self._placeholder = text
        self.update()

    def clearAllSelected(self) -> None:
        if not self._displayItems:
            return
        for item in self._displayItems:
            self.multiSelectionListWidget.item(self._items.index(item)).setChecked(False)
            self._widgetLayout.removeWidget(item)
            item.hide()
        self._displayItems.clear()
        self.selectedChange.emit(self._displayItems)

    def enableClearButton(self, enable: bool) -> None:
        if self.__enableClearButton == enable:
            return
        self.__enableClearButton = enable
        self.clearButton.setVisible(enable)

    def addItem(self, text: str) -> None:
        if text in self._texts:
            return
        self.multiSelectionListWidget.addItem(text)
        item = MultiSelectionItem(text, self)
        self._texts.append(text)
        self._items.append(item)
        item.hide()
        item.removeSignal.connect(self.updateCheckedState)

    def addItems(self, texts: List[str]) -> None:
        for text in texts:
            self.addItem(text)

    def removeItem(self, item: str):
        if item not in self._texts:
            return False
        index = self._texts.index(item)
        self._texts.remove(item)
        item = self._items[index]
        self.multiSelectionListWidget.takeItem(index)
        self._widgetLayout.removeWidget(item)
        self._items.remove(item)
        if item in self._displayItems:
            self._displayItems.remove(item)
        item.deleteLater()
        self._menu.adjustSize()
        self.selectedChange.emit(self._displayItems)
        return True

    def items(self) -> List[MultiSelectionItem]:
        return self._items

    def displayItems(self) -> List[MultiSelectionItem]:
        return self._displayItems

    def placeholderText(self) -> str:
        return self._placeholder

    def mouseReleaseEvent(self, event):
        self._showMenu()
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._menu.setFixedWidth(self.width())
        self._menu.view.setFixedWidth(self.width())
        self._menu.adjustSize()
        self._menu.view.adjustSize()
        self.multiSelectionListWidget.adjustSize()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        isDark = isDarkTheme()
        c = 32 if isDark else 255
        painter.setBrush(QColor(c, c, c))
        painter.setPen(QColor(c, c, c, 128))
        painter.drawRoundedRect(self.rect(), 6, 6)
        if not self.__hasItem:
            c = 255 if isDark else 0
            painter.setPen(QColor(c, c, c, 128))
            painter.drawText(self.rect().adjusted(10, 0, 0, 0), Qt.AlignVCenter, self._placeholder)