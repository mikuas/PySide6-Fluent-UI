# coding:utf-8
from enum import Enum
from typing import Union, List

from PySide6.QtCore import Qt, QSize, QPropertyAnimation, QPoint, QTimer, QObject, QEvent, Signal, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtWidgets import QFrame,  QGraphicsOpacityEffect, QWidget, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect

from .button import TransparentToolButton
from .label import BodyLabel
from ...common.auto_wrap import TextWrap
from ...common.icon import isDarkTheme, FluentIcon
from ...common.font import setFont


class ToastInfoBarColor(Enum):
    """ toast infoBar color """
    SUCCESS = '#0F7B0F'
    ERROR = '#BC0E11'
    WARNING = '#FCE100'
    INFO = '#2196F3'

    def __new__(cls, color):
        obj = object.__new__(cls)
        obj.color = QColor(color)
        return obj

    @property
    def value(self):
        return self.color


class ToastInfoBarPosition(Enum):
    """ toast infoBar position """
    TOP = 0
    BOTTOM = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5


class ToastInfoBar(QFrame):
    """ toast infoBar """
    def __init__(
            self,
            title: str,
            content: str,
            duration: int,
            isClosable: bool,
            position: ToastInfoBarPosition,
            orient: Qt.Orientation,
            toastColor: Union[str, QColor, ToastInfoBarColor],
            parent: QWidget,
            backgroundColor: QColor = None
    ):
        super().__init__(parent)
        parent.installEventFilter(self)
        self.title: str = title
        self.content: str = content
        self.duration: int = duration
        self.isCloseable: bool = isClosable
        self.orient: Qt.Orientation = orient
        self.toastColor: QColor = toastColor if isinstance(toastColor, QColor) else QColor(toastColor)
        self.position: ToastInfoBarPosition = position
        self.backgroundColor: QColor = backgroundColor

        self.titleLabel: BodyLabel = BodyLabel(self)
        self.contentLabel: BodyLabel = BodyLabel(self)
        self.closeButton: TransparentToolButton = TransparentToolButton(FluentIcon.CLOSE, self)

        self.hBoxLayout: QHBoxLayout = QHBoxLayout(self)
        if orient == Qt.Horizontal:
            self.textLayout: QHBoxLayout = QHBoxLayout()
            self.widgetLayout: QHBoxLayout = QHBoxLayout()
        else:
            self.textLayout: QVBoxLayout = QVBoxLayout()
            self.widgetLayout: QVBoxLayout = QVBoxLayout()

        self.__posAni: QPropertyAnimation = QPropertyAnimation(self, b'pos')
        self.__posAni.setEasingCurve(QEasingCurve.OutQuad)
        self.__posAni.setDuration(200)

        self._adjustText()
        self.__initWidget()
        self.__initShadowEffect()
        self.manager: ToastInfoBarManager = ToastInfoBarManager.get(self.position)
        
    def __initWidget(self):
        self.closeButton.setFixedSize(36, 36)
        self.closeButton.setIconSize(QSize(15, 15))
        self.closeButton.setCursor(Qt.PointingHandCursor)
        self.closeButton.setVisible(self.isCloseable)
        self.closeButton.clicked.connect(self.close)

        setFont(self.titleLabel, 16, QFont.DemiBold)
        setFont(self.contentLabel)
        self.__initLayout()
    
    def __initLayout(self):
        self.hBoxLayout.setContentsMargins(8, 8, 8, 8)
        self.hBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.textLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)
        self.textLayout.setAlignment(Qt.AlignTop)
        self.textLayout.setContentsMargins(1, 8, 0, 8)

        self.hBoxLayout.setSpacing(0)
        self.textLayout.setSpacing(5)

        self.textLayout.addWidget(self.titleLabel, 1, Qt.AlignTop)
        self.titleLabel.setVisible(bool(self.title))

        if self.orient == Qt.Horizontal:
            self.textLayout.addSpacing(7)

        self.textLayout.addWidget(self.contentLabel, 1, Qt.AlignTop)
        self.contentLabel.setVisible(bool(self.content))
        self.hBoxLayout.addLayout(self.textLayout)

        if self.orient == Qt.Horizontal:
            self.hBoxLayout.addLayout(self.widgetLayout)
            self.widgetLayout.setSpacing(10)
        else:
            self.textLayout.addLayout(self.widgetLayout)

        self.hBoxLayout.addSpacing(12)
        self.hBoxLayout.addWidget(self.closeButton, 0, Qt.AlignTop | Qt.AlignLeft)

    def __initShadowEffect(self):
        self.shadowEffect: QGraphicsDropShadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(24)
        self.shadowEffect.setOffset(0, 6)
        self.shadowEffect.setColor(QColor(0, 0, 0, 64))
        self.setGraphicsEffect(self.shadowEffect)

    def run(self):
        self.__posAni.setStartValue(self.startPosition)
        self.__posAni.setEndValue(self.endPosition)
        self.__posAni.start()

    def _adjustText(self):
        width = self.parent().width() / 1.5

        chars = max(min(width / 10, 120), 30)
        self.titleLabel.setText(TextWrap.wrap(self.title, chars, False)[0])

        chars = max(min(width / 9, 120), 30)
        self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])
        self.adjustSize()

    @classmethod
    def new(
            cls,
            title: str,
            content: str,
            duration: int,
            isClosable: bool,
            position: ToastInfoBarPosition,
            orient=Qt.Horizontal,
            toastColor: Union[str, QColor, ToastInfoBarColor] = ToastInfoBarColor.SUCCESS,
            parent: QWidget = None,
            backgroundColor: QColor = None,
    ):
        toastInfoBar = ToastInfoBar(
            title, content, duration, isClosable, position, orient, toastColor, parent, backgroundColor
        )
        toastInfoBar.show()
        return toastInfoBar

    @classmethod
    def info(
            cls,
            title: str,
            content: str,
            duration: int = 2000,
            isClosable: bool = True,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient: Qt.Orientation = Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(
            title, content, duration, isClosable, position, orient, ToastInfoBarColor.INFO.value, parent
        )

    @classmethod
    def success(
            cls,
            title: str,
            content: str,
            duration: int = 2000,
            isClosable: bool = True,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(
            title, content, duration, isClosable, position, orient, ToastInfoBarColor.SUCCESS.value, parent
        )

    @classmethod
    def warning(
            cls,
            title: str,
            content: str,
            duration: int = 2000,
            isClosable: bool = True,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(
            title, content, duration, isClosable, position, orient, ToastInfoBarColor.WARNING.value, parent
        )

    @classmethod
    def error(
            cls,
            title: str,
            content: str,
            duration: int = -1,
            isClosable: bool = True,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
    ):
        return cls.new(
            title, content, duration, isClosable, position, orient, ToastInfoBarColor.ERROR.value, parent
        )

    @classmethod
    def custom(
            cls,
            title: str,
            content: str,
            duration: int = 2000,
            isClosable: bool = True,
            position: ToastInfoBarPosition = ToastInfoBarPosition.TOP_RIGHT,
            orient=Qt.Horizontal,
            parent: QWidget = None,
            toastColor: Union[str, QColor] = None,
            backgroundColor: QColor = None
    ):
        return cls.new(
            title, content, duration, isClosable, position, orient, toastColor, parent, backgroundColor
        )

    def addWidget(self, widget: QWidget, stretch=0, alignment=Qt.AlignmentFlag):
        self.widgetLayout.addSpacing(6)
        self.widgetLayout.addWidget(widget, stretch, alignment)
        self.adjustSize()

    def showEvent(self, event):
        self._adjustText()
        super().showEvent(event)
        self.manager.add(self)
        self.startPosition = self.manager.slideStartPos(self)
        self.endPosition = self.manager.slideEndPos(self)
        self.run()

        if self.duration >= 0:
            QTimer.singleShot(self.duration, self.close)

    def closeEvent(self, event):
        self.manager.remove(self)
        self.setParent(None)
        self.deleteLater()
        super().closeEvent(event)
        del self

    def eventFilter(self, obj, event):
        if obj is self.parent() and event.type() in [QEvent.Resize, QEvent.WindowStateChange]:
            try:
                self._adjustText()
                self.move(self.manager.slideEndPos(self))
            except Exception: ...
        return super().eventFilter(obj, event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.toastColor)
        w, h = self.width(), self.height()
        painter.drawRoundedRect(0, 0, w, h - 4, 8, 8)

        painter.setBrush(self.backgroundColor or (QColor("#323232") if isDarkTheme() else QColor("#FFFFFF")))
        painter.drawRoundedRect(0, 5, w, h - 5, 6, 6)


class ToastInfoBarManager(QObject):
    """ ToastInfoBar manager """
    _instance = None
    registry = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ToastInfoBarManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False

        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        super().__init__()
        self.margin: int = 24
        self.toastInfoBars: List[ToastInfoBar] = []
        self.__initialized: bool = True

    def add(self, infoBar: ToastInfoBar):
        if infoBar in self.toastInfoBars:
            # print("存在")
            return
        # print(f"Add InfoBar: {infoBar}, ObjectName: {len(self.toastInfoBars) + 1}")
        # infoBar.setObjectName(str(len(self.toastInfoBars) + 1))
        # print(f"不存在, {infoBar in self.toastInfoBars}{infoBar.objectName()}")
        self.toastInfoBars.append(infoBar)

    def remove(self, infoBar: ToastInfoBar):
        self.toastInfoBars.remove(infoBar)
        # print(f"Remove: {infoBar},\nObjectName: {infoBar.objectName()}")
        self._adjustPosition()

    def _adjustPosition(self):
        # print(f"AdjustPosition: {"\n".join(str(_) for _ in self.toastInfoBars)}")
        # print(f"Length: {len(self.toastInfoBars)}")
        for bar in self.toastInfoBars:
            # print(f"For ObjectName: {bar.objectName()}")
            bar.startPosition, bar.endPosition = bar.pos(), self.slideEndPos(bar)
            bar.run()
        # print("\n")

    @classmethod
    def register(cls, element):
        def decorator(classType):
            cls.registry[element] = classType
            return classType

        return decorator

    @classmethod
    def get(cls, operation):
        if operation not in cls.registry:
            raise ValueError(f"No operation registered for {operation}")
        return cls.registry[operation]()

    def slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        raise NotImplementedError
    
    def slideEndPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        raise NotImplementedError


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP)
class TopToastInfoBarManager(ToastInfoBarManager):

    def slideEndPos(self, toastInfoBar):
        x = (toastInfoBar.parent().width() - toastInfoBar.width()) // 2
        y = self.margin / 2.5
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y += bar.height() + self.margin
        return QPoint(x, y + self.margin)

    def slideStartPos(self, toastInfoBar) -> QPoint:
        pos = self.slideEndPos(toastInfoBar)
        return QPoint(pos.x(), pos.y() - toastInfoBar.height() // 3)


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP_LEFT)
class TopLeftToastInfoBarManager(ToastInfoBarManager):

    def slideEndPos(self, toastInfoBar):
        x = self.margin
        y = self.margin / 2.5
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y += bar.height() + self.margin
        return QPoint(x, y + self.margin)

    def slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        pos = self.slideEndPos(toastInfoBar)
        return QPoint(-toastInfoBar.width(), pos.y())


@ToastInfoBarManager.register(ToastInfoBarPosition.TOP_RIGHT)
class TopRightToastInfoBarManager(ToastInfoBarManager):

    def slideEndPos(self, toastInfoBar):
        x = toastInfoBar.parent().width() - toastInfoBar.width() - self.margin
        y = self.margin / 2.5
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y += bar.height() + self.margin
        return QPoint(x, y + self.margin)

    def slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        pos = self.slideEndPos(toastInfoBar)
        return QPoint(toastInfoBar.parent().width() + toastInfoBar.width(), pos.y())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM)
class BottomToastInfoBarManager(ToastInfoBarManager):

    def slideEndPos(self, toastInfoBar):
        parent = toastInfoBar.parent()
        x = (parent.width() - toastInfoBar.width()) // 2
        y = parent.height() - self.margin
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y -= bar.height() + self.margin
        return QPoint(x, y - toastInfoBar.height())

    def slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        pos = self.slideEndPos(toastInfoBar)
        return QPoint(pos.x(), pos.y() + toastInfoBar.height() // 3)


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM_LEFT)
class BottomLeftToastInfoBarManager(ToastInfoBarManager):

    def slideEndPos(self, toastInfoBar):
        x = self.margin
        y = toastInfoBar.parent().height() - self.margin
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y -= bar.height() + self.margin
        return QPoint(x, y - toastInfoBar.height())

    def slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        pos = self.slideEndPos(toastInfoBar)
        return QPoint(-toastInfoBar.width(), pos.y())


@ToastInfoBarManager.register(ToastInfoBarPosition.BOTTOM_RIGHT)
class BottomRightToastInfoBarManager(ToastInfoBarManager):

    def slideEndPos(self, toastInfoBar):
        parent = toastInfoBar.parent()
        x = parent.width() - toastInfoBar.width() - self.margin
        y = parent.height() - self.margin
        for bar in self.toastInfoBars[:self.toastInfoBars.index(toastInfoBar)]:
            y -= bar.height() + self.margin
        return QPoint(x, y - toastInfoBar.height())

    def slideStartPos(self, toastInfoBar: ToastInfoBar) -> QPoint:
        pos = self.slideEndPos(toastInfoBar)
        return QPoint(toastInfoBar.parent().width() + self.margin, pos.y())