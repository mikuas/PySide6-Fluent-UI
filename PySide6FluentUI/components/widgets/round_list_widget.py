# coding:utf-8
from typing import Union

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

    def sizeHint(self, option, index):
        return QSize(0, 45)

    def paint(self, painter, option, index):
        painter.save()

        rect = option.rect.adjusted(2, 2, -2, -2) # type: QRect
        isDark = isDarkTheme()
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        pen = QPen()
        pen.setWidthF(1.4)
        if option.state & (QStyle.StateFlag.State_Selected | QStyle.StateFlag.State_MouseOver):
            pen.setColor(self._borderColor or themeColor())
            if isDark:
                fc = 32
                alpha = 32
            else:
                fc = 243
                alpha = 170
            painter.fillRect(rect.adjusted(1, 1, -1, -1), QColor(fc, fc, fc, alpha))
        else:
            if isDark:
                pc = 58
                fc = 0
                alpha = 32
            else:
                pc = 214
                fc = 255
                alpha = 170
            pen.setColor(QColor(pc, pc, pc, 114))
            painter.fillRect(rect.adjusted(1, 1, -1, -1), QColor(fc, fc, fc, alpha))
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


class RoundListBase:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.itemDelegate: RoundListWidgetItemDelegate = RoundListWidgetItemDelegate(self)
        self.scrollDelegate: SmoothScrollDelegate = SmoothScrollDelegate(self)

        self.setMouseTracking(True)
        self.setContentsMargins(24, 24, 24, 24)
        self.setSpacing(2)
        self.setItemDelegate(self.itemDelegate)

    def setItemBorderColor(self, color: Union[str, QColor]):
        self.itemDelegate.setBorderColor(color)


class RoundListWidget(RoundListBase, QListWidget):
    def __init__(self, parent=None):
        """
        RoundListWidget
        """
        super().__init__(parent)
        self.__editItem: QListWidgetItem = None
        self.setStyleSheet("RoundListWidget {background: transparent; border: none; padding: 10px;}")

    def __onDoubleItem(self, item):
        self.openPersistentEditor(item)
        self.__editItem = item

    def __onCloseEdit(self):
        if self.__editItem:
            self.closePersistentEditor(self.__editItem)

    def enableDoubleItemEdit(self, enable: bool):
        if enable:
            self.itemDoubleClicked.connect(self.__onDoubleItem)
            self.currentItemChanged.connect(self.__onCloseEdit)
        else:
            self.itemDoubleClicked.disconnect(self.__onDoubleItem)
            self.currentItemChanged.disconnect(self.__onCloseEdit)

    def setItemHeight(self, height: int):
        for i in range(self.count()):
            self.item(i).setSizeHint(QSize(0, height))

    def setItemTextAlignment(self, alignment: Qt.AlignmentFlag):
        for i in range(self.count()):
            self.item(i).setTextAlignment(alignment)


class RoundListView(RoundListBase, QListView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("RoundListView {background: transparent; border: none; padding: 10px;}")