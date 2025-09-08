# coding:utf-8
from typing import List, Union

from PySide6.QtGui import QFont, Qt, QPainter, QColor, QPen
from PySide6.QtCore import QSize, QRect
from PySide6.QtWidgets import QStyle, QListWidget, QListWidgetItem, QStyledItemDelegate, QListView

from ...common.color import themeColor, isDarkTheme
from ..widgets.scroll_area import SmoothScrollDelegate
from .line_edit import LineEdit


class RoundListWidgetItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._borderColor = None    # type: QColor

    def createEditor(self, parent, option, index):
        editor = LineEdit(parent)
        editor.setProperty("transparent", False)
        editor.setFixedHeight(option.rect.height() - 4)
        editor.setClearButtonEnabled(True)
        return editor

    def updateEditorGeometry(self, editor, option, index):
        rect = option.rect
        y = rect.y() + (rect.height() - editor.height()) // 2 + 1
        x, w = max(4, rect.x()), rect.width() - 4

        editor.setGeometry(x, y, w, rect.height())

    def setEditorData(self, editor, index):
        editor.setText(index.model().data(index, Qt.EditRole))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)

    def setBorderColor(self, color: Union[str, QColor]):
        if isinstance(color, str):
            color = QColor(color)
        self._borderColor = color

    def paint(self, painter, option, index):
        painter.save()

        rect = option.rect.adjusted(2, 2, -2, -2) # type: QRect
        isDark = isDarkTheme()
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        pen = QPen()
        pen.setWidthF(1.4)
        if option.state & (QStyle.StateFlag.State_Selected | QStyle.StateFlag.State_MouseOver):
            pen.setColor(self._borderColor or themeColor())
            painter.fillRect(rect.adjusted(1, 1, -1, -1), QColor("#2a2a2a") if isDark else QColor("#ebedf1"))
        else:
            painter.fillRect(rect.adjusted(1, 1, -1, -1), QColor("#2b2b2b") if isDark else QColor("#fafbfc"))
            pen.setColor(QColor("#3A3A3A") if isDark else QColor("#D7D6D6"))
        painter.setPen(pen)
        painter.drawRoundedRect(rect, 8, 8)

        alignment = index.data(Qt.TextAlignmentRole) or Qt.AlignLeft | Qt.AlignVCenter
        margin = self._drawIcon(painter, rect, index) or 10
        text = index.data()

        c = 255 if isDark else 0
        painter.setPen(QColor(c, c, c))
        painter.setFont(QFont("Microsoft YaHei UI", 10))
        painter.drawText(rect.adjusted(margin, 0, -10, 0), alignment, text)

        painter.restore()

    def _drawIcon(self, painter, rect, index):
        icon = index.data(Qt.DecorationRole)
        if icon:
            icon.paint(painter, rect.adjusted(10, 10, -10, -10), Qt.AlignLeft | Qt.AlignVCenter)
            return icon.pixmap(28, 28).width()


class RoundListWidget(QListWidget):
    def __init__(self, parent=None):
        """
        RoundListWidget
        """
        super().__init__(parent)
        self.__items: List[QListWidgetItem] = []
        self.__oldItem: QListWidgetItem = None
        self.itemDelegate: RoundListWidgetItemDelegate = RoundListWidgetItemDelegate(self)
        self.scrollDelegate: SmoothScrollDelegate = SmoothScrollDelegate(self)

        self.setMouseTracking(True)
        self.setSpacing(2)
        self.setItemDelegate(self.itemDelegate)
        self.setStyleSheet("RoundListWidget {background: transparent; border: none;}")

    def __onDoubleItem(self, item):
        self.openPersistentEditor(item)
        self.__oldItem = item

    def __onCloseEdit(self):
        if self.__oldItem:
            self.closePersistentEditor(self.__oldItem)

    def enableDoubleItemEdit(self, enable: bool):
        if enable:
            self.itemDoubleClicked.connect(self.__onDoubleItem)
            self.currentItemChanged.connect(self.__onCloseEdit)
        else:
            self.itemDoubleClicked.disconnect(self.__onDoubleItem)
            self.currentItemChanged.disconnect(self.__onCloseEdit)

    def setItemBorderColor(self, color: Union[str, QColor]):
        self.itemDelegate.setBorderColor(color)

    def setItemHeight(self, height: int):
        for item in self.allItems():
            item.setSizeHint(QSize(0, height))

    def setItemTextAlignment(self, alignment: Qt.AlignmentFlag):
        for item in self.allItems():
            item.setTextAlignment(alignment)

    def allItems(self):
        return self.__items

    def addItem(self, item: str | QListWidgetItem):
        if isinstance(item, str):
            item = QListWidgetItem(item)
        item.setSizeHint(QSize(0, 45))
        super().addItem(item)
        self.__items.append(item)

    def addItems(self, items: list[str] | list[QListWidgetItem]):
        for item in items:
            self.addItem(item)

    def insertItem(self, row: int, item: str | QListWidgetItem):
        if isinstance(item, str):
            item = QListWidgetItem(item)
        item.setSizeHint(QSize(0, 45))
        self.__items.append(item)
        super().insertItem(row, item)

    def insertItems(self, row, items: Union[List[str,], List[QListWidgetItem]]):
        for item in items:
            self.insertItem(row, item)


class RoundListView(QListView):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.itemDelegate: RoundListWidgetItemDelegate = RoundListWidgetItemDelegate(self)
        self.scrollDelegate: SmoothScrollDelegate = SmoothScrollDelegate(self)

        self.setItemDelegate(self.itemDelegate)
        self.setMouseTracking(True)
        self.setSpacing(2)
        self.setStyleSheet("RoundListView {background: transparent; border: none;}")