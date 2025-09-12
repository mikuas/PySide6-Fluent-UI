# coding:utf-8
from PySide6.QtCore import Qt
from PySide6FluentUI import FillPushButton, ToastInfoBar, ToastInfoBarColor, ToastInfoBarPosition, themeColor
from ..widgets.basic_interface import Interface
from ..widgets.widget_item import StandardItem


class StatusInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("状态和信息", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("StatusInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

        self.toastInfoBarItem: StandardItem = StandardItem("吐司提示", self)
        self.successToastButton: FillPushButton = FillPushButton("成功", self)
        self.errorToastButton: FillPushButton = FillPushButton("失败", self)
        self.warningToastButton: FillPushButton = FillPushButton("警告", self)
        self.infoToastButton: FillPushButton = FillPushButton("信息", self)
        self.customToastButton: FillPushButton = FillPushButton("自定义", self)

        self.successToastButton.setFillColor(ToastInfoBarColor.SUCCESS.value)
        self.successToastButton.setFixedWidth(64)
        self.errorToastButton.setFillColor(ToastInfoBarColor.ERROR.value)
        self.errorToastButton.setFixedWidth(64)
        self.warningToastButton.setFillColor(ToastInfoBarColor.WARNING.value)
        self.warningToastButton.setFixedWidth(64)
        self.infoToastButton.setFillColor(ToastInfoBarColor.INFO.value)
        self.infoToastButton.setFixedWidth(64)
        self.customToastButton.setFixedWidth(82)

        self.toastInfoBarItem.card.setFixedHeight(114)
        self.toastInfoBarItem.addWidget(self.successToastButton)
        self.toastInfoBarItem.addWidget(self.errorToastButton)
        self.toastInfoBarItem.addWidget(self.warningToastButton)
        self.toastInfoBarItem.addWidget(self.infoToastButton)
        self.toastInfoBarItem.addWidget(self.customToastButton)

        self.scrollLayout.addWidget(self.toastInfoBarItem)

        self.connectSignalSlot()

    def connectSignalSlot(self):
        self.successToastButton.clicked.connect(
            lambda: ToastInfoBar.success(
                "Lesson",
                "最短的捷径就是绕远路,绕远路才是我最短的捷径",
                duration=3000,
                orient=Qt.Orientation.Vertical,
                position=ToastInfoBarPosition.TOP,
                parent=self.window()
            )
        )
        self.errorToastButton.clicked.connect(
            lambda: ToastInfoBar.error(
                "Title",
                "最短的捷径就是绕远路,绕远路才是我最短的捷径",
                duration=-1,
                orient=Qt.Orientation.Vertical,
                position=ToastInfoBarPosition.TOP_RIGHT,
                parent=self.window()
            )
        )
        self.warningToastButton.clicked.connect(
            lambda: ToastInfoBar.warning(
                "Title",
                "最短的捷径就是绕远路,绕远路才是我最短的捷径",
                duration=3000,
                orient=Qt.Orientation.Vertical,
                position=ToastInfoBarPosition.TOP_LEFT,
                parent=self.window()
            )
        )
        self.infoToastButton.clicked.connect(
            lambda: ToastInfoBar.info(
                "Title",
                "最短的捷径就是绕远路,绕远路才是我最短的捷径",
                duration=3000,
                orient=Qt.Orientation.Vertical,
                position=ToastInfoBarPosition.BOTTOM_RIGHT,
                parent=self.window()
            )
        )
        self.customToastButton.clicked.connect(
            lambda: ToastInfoBar.custom(
                "Title",
                "最短的捷径就是绕远路,绕远路才是我最短的捷径",
                duration=3000,
                orient=Qt.Orientation.Vertical,
                position=ToastInfoBarPosition.BOTTOM,
                parent=self.window(),
                toastColor=themeColor()
            )
        )