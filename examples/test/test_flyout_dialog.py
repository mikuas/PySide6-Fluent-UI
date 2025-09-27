# coding:utf-8
import sys
from enum import Enum
from typing import Tuple
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QPoint, QEasingCurve

from PySide6FluentUI import SplitWidget, PopupView, BodyLabel, HorizontalSeparator, TransparentToolButton, \
    FluentIcon, StrongBodyLabel, PushButton


class FlyoutPosition(Enum):

    TOP = 1
    LEFT = 2
    RIGHT = 3
    BOTTOM = 4


class FlyoutDialog(PopupView):
    def __init__(self, target: QWidget, position: FlyoutPosition = FlyoutPosition.TOP, parent=None, layout=QVBoxLayout):
        super().__init__(parent, layout)
        self.posAni.setEasingCurve(QEasingCurve.OutQuart)
        self.target: QWidget = target
        self.positionManager: FlyoutDialogManager = FlyoutDialogManager.get(position, self)

    def show(self):
        self.adjustSize()
        if self.isVisible():
            self.hide()
        self.exec(*self.positionManager.pos())


class FlyoutDialogManager:
    registry = {}

    def __init__(self, view: FlyoutDialog):
        super().__init__()
        self.view: FlyoutDialog = view

    @classmethod
    def register(cls, element):
        def decorator(classType):
            cls.registry[element] = classType
            return classType

        return decorator

    @classmethod
    def get(cls, operation, view):
        if operation not in cls.registry:
            raise ValueError(f"No operation registered for {operation}")
        return cls.registry[operation](view)

    def pos(self) -> Tuple[QPoint, QPoint]:
        raise NotImplementedError


@FlyoutDialogManager.register(FlyoutPosition.TOP)
class TopFlyoutDialogManager(FlyoutDialogManager):

    def pos(self) -> Tuple[QPoint, QPoint]:
        pos = self.view.target.mapToGlobal(self.view.target.rect().topLeft())
        x, y = pos.x(), pos.y()
        x -= (self.view.width() - self.view.target.width()) // 2
        y -= self.view.height()

        return QPoint(x, y + 12), QPoint(x, y)


@FlyoutDialogManager.register(FlyoutPosition.BOTTOM)
class BottomFlyoutDialogManager(FlyoutDialogManager):

    def pos(self) -> Tuple[QPoint, QPoint]:
        pos = self.view.target.mapToGlobal(self.view.target.rect().bottomLeft())
        x, y = pos.x(), pos.y()
        x -= (self.view.width() - self.view.target.width()) // 2

        return QPoint(x, y - 12), QPoint(x, y)


@FlyoutDialogManager.register(FlyoutPosition.LEFT)
class LeftFlyoutDialogManager(FlyoutDialogManager):

    def pos(self) -> Tuple[QPoint, QPoint]:
        pos = self.view.target.mapToGlobal(self.view.target.rect().topLeft())
        x, y = pos.x(), pos.y()
        x -= self.view.width()
        y -= (self.view.height() - self.view.target.height()) // 2

        return QPoint(x + 12, y), QPoint(x, y)


@FlyoutDialogManager.register(FlyoutPosition.RIGHT)
class RightFlyoutDialogManager(FlyoutDialogManager):

    def pos(self) -> Tuple[QPoint, QPoint]:
        pos = self.view.target.mapToGlobal(self.view.target.rect().topRight())
        x, y = pos.x(), pos.y()
        y -= (self.view.height() - self.view.target.height()) // 2

        return QPoint(x - 12, y), QPoint(x, y)


class Window(SplitWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(11, 38, 11, 11)
        self.layout().setAlignment(Qt.AlignCenter)

        self.__initWidget()
        self.connectSignalSlot()

    def __initWidget(self):
        self.button1: PushButton = PushButton("show dialog", self)
        self.button2: PushButton = PushButton("show dialog", self)
        self.flyoutDialog: FlyoutDialog = FlyoutDialog(self.button1, position=FlyoutPosition.RIGHT, parent=self)
        self.titleLabel: StrongBodyLabel = StrongBodyLabel("   无名", self)
        self.contentLabel: BodyLabel = BodyLabel("     左眼用来忘记你，右眼用来记住你。    ", self)
        self.yesBtn: TransparentToolButton = TransparentToolButton(FluentIcon.ACCEPT, self)
        self.closeBtn: TransparentToolButton = TransparentToolButton(FluentIcon.CLOSE, self)

        self.button1.setFixedSize(328, 35)
        self.button2.setFixedSize(328, 35)
        self.titleLabel.setFontSize(22)
        self.yesBtn.setFixedHeight(35)
        self.closeBtn.setFixedHeight(35)
        self.yesBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.closeBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.__initLayout()

    def __initLayout(self):
        self.layout().addWidget(self.button1)
        self.layout().addWidget(self.button2)

        self.flyoutDialog.viewLayout.addWidget(self.titleLabel)
        self.flyoutDialog.viewLayout.addSpacing(5)
        self.flyoutDialog.viewLayout.addWidget(self.contentLabel)
        self.flyoutDialog.viewLayout.addSpacing(10)
        self.flyoutDialog.viewLayout.addWidget(HorizontalSeparator(self))
        self.flyoutDialog.viewLayout.setContentsMargins(1, 10, 1, 0)

        self.hBoxLayout = QHBoxLayout()
        self.flyoutDialog.viewLayout.addLayout(self.hBoxLayout, 1)
        self.hBoxLayout.addWidget(self.yesBtn, 1)
        self.hBoxLayout.addWidget(self.closeBtn, 1)

    def connectSignalSlot(self):
        self.button1.clicked.connect(lambda: {
            self.updateTarget(self.button1),
            self.flyoutDialog.show()
        })
        self.button2.clicked.connect(lambda: {
            self.updateTarget(self.button2),
            self.flyoutDialog.show()
        })
        self.yesBtn.clicked.connect(self.flyoutDialog.hide)
        self.closeBtn.clicked.connect(self.flyoutDialog.hide)

    def updateTarget(self, target: QWidget):
        self.flyoutDialog.target = target


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.resize(800, 520)
    window.show()
    sys.exit(app.exec())
    
    ...

if __name__ == '__main__':
    main()