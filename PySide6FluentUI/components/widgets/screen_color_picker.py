# coding:utf-8
from typing import Union
from pynput import mouse

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsDropShadowEffect, QHBoxLayout, QLayout, \
    QFrame
from PySide6.QtCore import Qt, QTimer, QRect, QSize, QThread, Signal, QPoint
from PySide6.QtGui import QGuiApplication, QCursor, QPainter, QColor

from .drop_down_color_palette import BaseItem, ColorView
from .popup_view import FrameView
from .label import BodyLabel
from .button import TransparentToolButton
from ...common.icon import FluentIcon
from ...common.style_sheet import isDarkTheme


class MouseListenerThread(QThread):
    clicked = Signal()

    def run(self):

        def onClick(x, y, button, pressed):
            if pressed:
                self.clicked.emit()
                return False
        with mouse.Listener(on_click=onClick) as listener:
            listener.join()


class ScreenColorPickerView(FrameView):
    def __init__(self, parent):
        super().__init__(parent, QHBoxLayout)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
        self.viewLayout.setContentsMargins(5, 5, 5, 5)
        self.viewLayout.setSpacing(10)

        self.nameLabel: BodyLabel = BodyLabel(self)
        self.color: QColor = QColor(255, 255, 255)
        self.colorItem: BaseItem = BaseItem(self.color, self)
        self.timer: QTimer = QTimer(self)
        self.thread: MouseListenerThread = MouseListenerThread(self)

        self.colorItem.setFixedSize(32, 32)
        self.viewLayout.addWidget(self.colorItem)
        self.viewLayout.addWidget(self.nameLabel)
        self.setMinimumSize(135, 46)

    def pickColor(self):
        pos = QCursor.pos()
        screen = QGuiApplication.primaryScreen()
        x, y = pos.x(), pos.y()
        self.color = screen.grabWindow(0, x, y, 1, 1).toImage().pixelColor(0, 0)
        self.nameLabel.setText(self.color.name())
        self.colorItem.setColor(self.color)
        self.raise_()
        self.move(x + 20, y + 20)

    def start(self, interval=10):
        self.move(QCursor.pos() + QPoint(20, 20))
        self.raise_()
        self.thread.start()
        self.timer.start(interval)
        self.show()

    def stop(self):
        self.timer.stop()
        self.close()

    def connectSignalSlot(self, onClicked):
        self.timer.timeout.connect(self.pickColor)
        self.thread.clicked.connect(onClicked)


class ScreenColorPicker(ColorView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.colorPickerView: ScreenColorPickerView = ScreenColorPickerView(self)
        self.setCurrentColor(self.colorPickerView.color)
        self.widgetLayout.setContentsMargins(5, 4, 5, 4)
        self.pickerColorButton.setIcon(FluentIcon.COLOR_PICKER)

        self.connectSignalSlot()

    def setDefaultColor(self, color: Union[str, QColor]):
        self.setCurrentColor(color)
        super().setDefaultColor(color)

    def start(self, interval=10):
        self.colorPickerView.start(interval)

    def stop(self):
        self.colorPickerView.stop()
        self.setDefaultColor(self.colorPickerView.color)
        self.colorChanged.emit(self.colorPickerView.color)

    def connectSignalSlot(self):
        self.pickerColorButton.clicked.connect(self.colorPickerView.start)
        self.colorPickerView.connectSignalSlot(self.stop)