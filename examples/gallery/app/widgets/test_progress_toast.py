# coding:utf-8
from typing import Union

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, Property, QPropertyAnimation, QRect, Signal, QEvent

from PySide6FluentUI import ToastInfoBar, isDarkTheme, ToastInfoBarPosition, ToastInfoBarColor, drawRoundRect


class ProgressToast(ToastInfoBar):

    progressChanged = Signal()

    def __init__(self, title, content, time: int,  position, orient, toastColor, parent, backgroundColor):
        super().__init__(
            title, content, duration=-1, isClosable=True, position=position,
            orient=orient, toastColor=toastColor, parent=parent, backgroundColor=backgroundColor
        )
        self._progress: int = 0
        self.__br: int = 0
        self.closeButton.setVisible(False)
        self.hBoxLayout.setContentsMargins(6, 6, 6, 16)

        self._progressAni: QPropertyAnimation = QPropertyAnimation(self, b'progress')
        self._progressAni.setStartValue(0)
        self._progressAni.setDuration(time)

        self.progressChanged.connect(self.update)
        self._progressAni.finished.connect(self.__onFinishedProgress)

    def _adjustText(self): ...

    def __onFinishedProgress(self):
        self.__br = 8
        self.closeButton.setVisible(True)
        self.setValue(self.width())
        self.update()
        self.move(self.manager.slideEndPos(self))

    def show(self):
        super()._adjustText()
        super().show()
        self._progressAni.setEndValue(self.width())
        self._progressAni.start()

    def getValue(self):
        return self._progress

    def setValue(self, value: int):
        if value == self._progress:
            return
        self.progressChanged.emit()
        self._progress = value

    @classmethod
    def new(
            cls,
            title: str,
            content: str,
            time: int,
            position: ToastInfoBarPosition,
            orient=Qt.Horizontal,
            toastColor: Union[str, QColor, ToastInfoBarColor] = ToastInfoBarColor.SUCCESS,
            parent: QWidget = None,
            backgroundColor: QColor = None,
    ):
        progressToast = ProgressToast(title, content, time, position, orient, toastColor, parent, backgroundColor)
        progressToast.show()
        return progressToast

    @classmethod
    def info(
            cls,
            title: str,
            content: str,
            time: int,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient: Qt.Orientation = Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(title, content, time, position, orient, ToastInfoBarColor.INFO.value, parent)

    @classmethod
    def success(
            cls,
            title: str,
            content: str,
            time: int,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(title, content, time, position, orient, ToastInfoBarColor.SUCCESS.value, parent)

    @classmethod
    def warning(
            cls,
            title: str,
            content: str,
            time: int,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(title, content, time, position, orient, ToastInfoBarColor.WARNING.value, parent)

    @classmethod
    def error(
            cls,
            title: str,
            content: str,
            time: int,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(title, content, time, position, orient, ToastInfoBarColor.ERROR.value, parent)

    @classmethod
    def custom(
            cls,
            title: str,
            content: str,
            time: int,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
            toastColor: Union[str, QColor] = None,
            backgroundColor: QColor = None
    ):
        return cls.new(title, content, time, position, orient, toastColor, parent, backgroundColor)

    def eventFilter(self, obj, event):
        if obj is self.parent() and event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            try:
                self.move(self.manager.slideEndPos(self))
            except Exception: ...
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        w, h = self.width(), self.height()

        painter.setBrush(self.backgroundColor or (QColor("#323232") if isDarkTheme() else QColor("#FFFFFF")))
        painter.drawRoundedRect(0, 0, w, h - 5, 6, 6)

        painter.setBrush(self.toastColor)
        drawRoundRect(painter, QRect(0, h - 10, self.getValue() + 1, 6), 0, 0, self.__br, 8)

    progress = Property(int, getValue, setValue)