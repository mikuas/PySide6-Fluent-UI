import sys
from typing import Union
from pynput import mouse

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsDropShadowEffect, QHBoxLayout, QLayout
from PySide6.QtCore import Qt, QTimer,  QRect, QSize, QThread, Signal
from PySide6.QtGui import QGuiApplication, QCursor, QPainter, QColor

from PySide6FluentUI import StandardItem, isDarkTheme, TransparentToolButton, FluentIcon, toggleTheme, SplitWidget


class MouseListenerThread(QThread):
    clicked = Signal()

    def run(self):

        def onClick(x, y, button, pressed):
            if pressed:
                self.clicked.emit()
                return False
        with mouse.Listener(on_click=onClick) as listener:
            listener.join()


class ScreenColorPickerView(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.color: QColor = QColor(255, 255, 255)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.timer: QTimer = QTimer(self)
        self.thread: MouseListenerThread = MouseListenerThread(self)

        self.__initShadowEffect()

    def __initShadowEffect(self):
        self.shadowEffect: QGraphicsDropShadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setOffset(0, 0)
        self.shadowEffect.setColor(QColor(0, 0, 0, 128))
        self.shadowEffect.setBlurRadius(24)

    def pickColor(self):
        pos = QCursor.pos()
        screen = QGuiApplication.primaryScreen()
        x, y = pos.x(), pos.y()
        self.color = screen.grabWindow(0, x, y, 1, 1).toImage().pixelColor(0, 0)
        self.update()
        self.raise_()
        self.move(x + 20, y + 20)

    def start(self, interval=10):
        self.show()
        self.raise_()
        self.thread.start()
        self.timer.start(interval)

    def stop(self):
        self.timer.stop()
        self.close()

    def sizeHint(self):
        return QSize(114, 46)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.TextAntialiasing | QPainter.Antialiasing)
        painter.setPen(QColor(0, 0, 0, 32))
        painter.setBrush(QColor(255, 255, 255))

        painter.drawRoundedRect(self.rect(), 8, 8)

        painter.setBrush(self.color)
        painter.drawRoundedRect(QRect(5, 5, 36, 36), 8, 8)
        painter.setPen(QColor(0, 0, 0))
        painter.drawText(self.rect().adjusted(58, 0, 0, 0), Qt.AlignVCenter, self.color.name())

    def connectSignalSlot(self, onClicked):
        self.timer.timeout.connect(self.pickColor)
        self.thread.clicked.connect(onClicked)


class ScreenColorPicker(QWidget):
    colorChanged = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.colorPickerView: ScreenColorPickerView = ScreenColorPickerView(self)
        self._currentColor: QColor = self.colorPickerView.color
        self.hBoxLayout: QHBoxLayout = QHBoxLayout(self)
        self.colorItem: StandardItem = StandardItem(self._currentColor)
        self.pickerButton: TransparentToolButton = TransparentToolButton(FluentIcon.EDIT, self)

        self.colorItem.setFixedSize(26, 26)
        self.__initLayout()

        self.pickerButton.clicked.connect(self.colorPickerView.start)
        self.colorPickerView.connectSignalSlot(self.stop)

    def __initLayout(self):
        self.hBoxLayout.setContentsMargins(5, 3, 5, 3)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.hBoxLayout.addWidget(self.colorItem)
        self.hBoxLayout.addWidget(self.pickerButton)

    def setDefaultColor(self, color: Union[str, QColor]):
        if isinstance(color, str):
            color = QColor(color)
        if color == self._currentColor:
            return
        self._currentColor = color
        self.colorItem.setColor(color)

    def currentColor(self) -> QColor:
        return self._currentColor

    def start(self, interval=10):
        self.colorPickerView.start(interval)

    def stop(self):
        self.colorPickerView.stop()
        self.setDefaultColor(self.colorPickerView.color)
        self.colorChanged.emit(self.colorPickerView.color)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        c = 255 if isDarkTheme() else 0
        painter.setPen(QColor(c, c, c, 32))
        painter.drawRoundedRect(self.rect().adjusted(2, 2, -2, -2), 8, 8)


class Window(SplitWidget):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        from PySide6FluentUI import DropDownColorPalette

        self.dcp = DropDownColorPalette(self)
        from PySide6FluentUI import ScreenColorPicker
        self.screenColorPicker = ScreenColorPicker(self)

        self.screenColorPicker.setDefaultColor("deeppink")
        self.box.addWidget(self.screenColorPicker)
        self.box.addWidget(self.dcp)

        self.dcp.colorItem.clicked.connect(lambda: {toggleTheme(), update(), self.toggleStayOnTop(), self.setMicaEffectEnabled(True)})

        self.screenColorPicker.colorChanged.connect(
            lambda color: {
                print(
                    f"{color} : {color.name()}",
                    "\n",
                    f"{self.screenColorPicker.currentColor()} : {self.screenColorPicker.currentColor().name()}",
                    "\n",
                    f"{self.screenColorPicker.colorPickerView.color} : {self.screenColorPicker.colorPickerView.color.name()}",
                    "\n",
                    color == self.screenColorPicker.currentColor() == self.screenColorPicker.colorPickerView.color,
                    "\n"
                )
            }
        )

def update():
    for w in QApplication.allWidgets():
        try:
            w.update()
        except TypeError:
            continue

if __name__ == "__main__":
    app = QApplication(sys.argv)
    picker = Window()
    picker.show()
    sys.exit(app.exec())
