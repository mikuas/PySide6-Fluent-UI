# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

from PySide6FluentUI import FillPushButton, ToastInfoBar, ToastInfoBarColor, ToastInfoBarPosition, themeColor, \
    MessageBoxBase, TransparentToolButton, FluentIcon, setToolTipInfo, ToolTipPosition, CaptionLabel, LineEdit, \
    ComboBox, ColorPickerButton

from ..widgets.basic_interface import Interface
from ..widgets.test_progress_toast import ProgressToast


class TextDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout.removeItem(self.viewLayout)
        self.viewLayout = QHBoxLayout()
        self.vBoxLayout.insertLayout(0, self.viewLayout, 1)

        self.viewLayout.setSpacing(12)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)
        self.hide()

        self.__initTextDialog()

    def __initTextDialog(self):
        self.textLayout = QVBoxLayout()
        self.comboBoxLayout = QVBoxLayout()
        self.viewLayout.addLayout(self.textLayout)
        self.viewLayout.addLayout(self.comboBoxLayout)

        self.titleEdit: LineEdit = LineEdit(self)
        self.textLayout.addWidget(CaptionLabel("设置消息条标题", self))
        self.textLayout.addWidget(self.titleEdit)

        self.connectEdit: LineEdit = LineEdit(self)
        self.textLayout.addWidget(CaptionLabel("设置消息条内容", self))
        self.textLayout.addWidget(self.connectEdit)

        self.durationComboBox: ComboBox = ComboBox(self)
        self.durationComboBox.addItems([str(_ * 100) for _ in range(51)])
        self.durationComboBox.setCurrentText("3000")
        self.comboBoxLayout.addWidget(CaptionLabel("持续时间(ms)", self))
        self.comboBoxLayout.addWidget(self.durationComboBox)

        self.orientComboBox: ComboBox = ComboBox(self)
        self.orientComboBox.addItems(["Qt.Orientation.Vertical", "Qt.Orientation.Horizontal"])
        self.comboBoxLayout.addWidget(CaptionLabel("消息条布局方向", self))
        self.comboBoxLayout.addWidget(self.orientComboBox)

        self.colorPickButton: ColorPickerButton = ColorPickerButton(themeColor(), "选择颜色", self, True)
        self.colorPickButton.setFixedWidth(256)
        self.textLayout.addWidget(CaptionLabel("选择自定义吐司条颜色", self), 1, Qt.AlignHCenter)
        self.comboBoxLayout.addWidget(self.colorPickButton)

        self.titleEdit.setFixedWidth(256)
        self.connectEdit.setFixedWidth(256)
        self.durationComboBox.setFixedWidth(256)
        self.orientComboBox.setFixedWidth(256)
        ...

    def validate(self) -> bool:
        return bool(self.titleEdit.text().strip()) and bool(self.connectEdit.text().strip())


class StatusInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("状态和信息", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("StatusInterface")
        self.vBoxLayout.addWidget(self.scrollArea)
        self.orients = [Qt.Orientation.Vertical, Qt.Orientation.Horizontal]

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        self.successToastButton: FillPushButton = FillPushButton("成功", self)
        self.errorToastButton: FillPushButton = FillPushButton("失败", self)
        self.warningToastButton: FillPushButton = FillPushButton("警告", self)
        self.infoToastButton: FillPushButton = FillPushButton("信息", self)
        self.customToastButton: FillPushButton = FillPushButton("自定义", self)
        self.editTextButton: TransparentToolButton = TransparentToolButton(FluentIcon.EDIT, self)
        self.textDialog: TextDialog = TextDialog(self.parent())

        self.textDialog.titleEdit.setText("Lesson")
        self.textDialog.connectEdit.setText("最短的捷径就是绕远路,绕远路才是我最短的捷径")
        self.successToastButton.setFillColor(ToastInfoBarColor.SUCCESS.value)
        self.successToastButton.setFixedWidth(64)
        self.errorToastButton.setFillColor(ToastInfoBarColor.ERROR.value)
        self.errorToastButton.setFixedWidth(64)
        self.warningToastButton.setFillColor(ToastInfoBarColor.WARNING.value)
        self.warningToastButton.setFixedWidth(64)
        self.infoToastButton.setFillColor(ToastInfoBarColor.INFO.value)
        self.infoToastButton.setFixedWidth(64)
        self.customToastButton.setFixedWidth(82)

        layout.addWidget(self.successToastButton)
        layout.addWidget(self.errorToastButton)
        layout.addWidget(self.warningToastButton)
        layout.addWidget(self.infoToastButton)
        layout.addWidget(self.customToastButton)
        layout.addWidget(self.editTextButton, 1, Qt.AlignRight | Qt.AlignVCenter)

        setToolTipInfo(self.editTextButton, "编辑", 3000, ToolTipPosition.TOP)
        self.addExamplesCard(
            "吐司提示",
            widget,
            1
        )

        self.progressButton: FillPushButton = FillPushButton("显示进度", self)
        self.addExamplesCard(
            "吐司任务进度条",
            self.progressButton,
        )

        self.scrollLayout.addStretch(1)
        self.connectSignalSlot()

    def connectSignalSlot(self):
        self.successToastButton.clicked.connect(
            lambda: ToastInfoBar.success(
                self.textDialog.titleEdit.text(),
                self.textDialog.connectEdit.text(),
                duration=int(self.textDialog.durationComboBox.currentText()),
                orient=self.orients[self.textDialog.orientComboBox.currentIndex()],
                position=ToastInfoBarPosition.TOP,
                parent=self
            )
        )
        self.errorToastButton.clicked.connect(
            lambda: ToastInfoBar.error(
                self.textDialog.titleEdit.text(),
                self.textDialog.connectEdit.text(),
                duration=-1,
                orient=self.orients[self.textDialog.orientComboBox.currentIndex()],
                position=ToastInfoBarPosition.TOP_RIGHT,
                parent=self
            )
        )
        self.warningToastButton.clicked.connect(
            lambda: ToastInfoBar.warning(
                self.textDialog.titleEdit.text(),
                self.textDialog.connectEdit.text(),
                duration=int(self.textDialog.durationComboBox.currentText()),
                orient=self.orients[self.textDialog.orientComboBox.currentIndex()],
                position=ToastInfoBarPosition.TOP_LEFT,
                parent=self
            )
        )
        self.infoToastButton.clicked.connect(
            lambda: ToastInfoBar.info(
                self.textDialog.titleEdit.text(),
                self.textDialog.connectEdit.text(),
                duration=int(self.textDialog.durationComboBox.currentText()),
                orient=self.orients[self.textDialog.orientComboBox.currentIndex()],
                position=ToastInfoBarPosition.BOTTOM_RIGHT,
                parent=self
            )
        )
        self.customToastButton.clicked.connect(
            lambda: ToastInfoBar.custom(
                self.textDialog.titleEdit.text(),
                self.textDialog.connectEdit.text(),
                duration=int(self.textDialog.durationComboBox.currentText()),
                orient=self.orients[self.textDialog.orientComboBox.currentIndex()],
                position=ToastInfoBarPosition.BOTTOM,
                parent=self,
                toastColor=self.textDialog.colorPickButton.color
            )
        )

        self.editTextButton.clicked.connect(self.textDialog.exec)
        # self.editTextButton.clicked.connect(self.textDialog.show)
        self.textDialog.colorPickButton.colorChanged.connect(self.customToastButton.setFillColor)

        self.progressButton.clicked.connect(
            lambda: ProgressToast.custom(
                self.textDialog.titleEdit.text(),
                self.textDialog.connectEdit.text(),
                time=int(self.textDialog.durationComboBox.currentText()),
                orient=self.orients[self.textDialog.orientComboBox.currentIndex()],
                position=ToastInfoBarPosition.TOP,
                toastColor=self.textDialog.colorPickButton.color,
                parent=self
            )
        )