# coding:utf-8
import sys

from PySide6.QtCore import QObject, Property, Signal, QTimer, QPropertyAnimation, Qt
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget


class QtProperty(QObject):

    valueChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self._value: int = 0

        self.valueChanged.connect(lambda: print(f"{self.value = }"))

    # @Property(int)
    # def value(self) -> int:
    #     return self._value
    #
    # @value.setter
    # def value(self, value: int):
    #     if value < 0 or value == self._value:
    #         return
    #     self._value = value
    #     self.valueChanged.emit(value)

    def getValue(self) -> int:
        return self._value

    def setValue(self, value: int) -> None:
        if value < 0 or value == self._value:
            return
        self._value = value
        self.valueChanged.emit(value)

    value = Property(int, getValue, setValue)


class Window(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setFixedHeight(25)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._property = None
        self._position = None

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self._position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.move(event.globalPosition().toPoint() - self._position)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor(0, 0, 0, 32))
        painter.setBrush(QColor("deeppink"))
        painter.drawRoundedRect(1, 1, self._property.value - 1, 24, 8, 8)


def qtProperDemo():
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    qtProperty = QtProperty()
    qtProperty.value = 10

    animation = QPropertyAnimation(qtProperty, b"value")
    animation.setStartValue(0)
    animation.setEndValue(1000)
    animation.setDuration(5000)

    window = Window()
    window._property = qtProperty
    window.setFixedWidth(animation.endValue() + 2)
    window.show()
    qtProperty.valueChanged.connect(window.update)

    animation.start()

    sys.exit(app.exec())


def main():
    qtProperDemo()


if __name__ == '__main__':
    main()

