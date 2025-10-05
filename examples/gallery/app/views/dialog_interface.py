# coding:utf-8
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QSizePolicy, QWidget, QHBoxLayout

from PySide6FluentUI import PopupDrawerWidget, PopupDrawerPosition, PushButton, DropDownColorPalette, ScreenColorPicker, \
    FlyoutDialog, StrongBodyLabel, BodyLabel, TransparentToolButton, FluentIcon, HorizontalSeparator, HBoxLayout, \
    SwitchButton, FlyoutPosition, LineEdit, PrimaryPushButton, ComboBox, ToastInfoBar, ToastInfoBarPosition

from ..widgets.basic_interface import Interface


class DrawerSettingView(FlyoutDialog):
    def __init__(self, target, parent=None):
        super().__init__(target, FlyoutPosition.LEFT, parent)
        self.parent = parent
        self.setFixedSize(414, 256)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)
        self.viewLayout.setSpacing(12)

        self.durationLayout: QHBoxLayout = QHBoxLayout()
        self.durationLabel: BodyLabel = BodyLabel("设置动画时长:", self)
        self.durationLineEdit: LineEdit = LineEdit(self)

        self.durationLineEdit.setFixedWidth(128)
        self.durationLineEdit.setValidator(QIntValidator(self))
        self.durationLayout.addWidget(self.durationLabel, 0, Qt.AlignLeft)
        self.durationLayout.addWidget(self.durationLineEdit, 1, Qt.AlignRight)

        self.clickOtherHideLayout: QHBoxLayout = QHBoxLayout()
        self.clickOtherHideLabel: BodyLabel = BodyLabel("启用点击其他隐藏:", self)
        self.clickOterHideSwitchButton: SwitchButton = SwitchButton(self)
        self.clickOterHideSwitchButton.setChecked(True)

        self.clickOterHideSwitchButton.setFixedWidth(128)
        self.clickOtherHideLayout.addWidget(self.clickOtherHideLabel, 0, Qt.AlignLeft)
        self.clickOtherHideLayout.addWidget(self.clickOterHideSwitchButton, 0, Qt.AlignRight)

        self.radius: List[str] = [str(r) for r in range(0, 25)]
        self.radiusLabel: BodyLabel = BodyLabel("设置圆角(左上, 右上, 右下, 左下)", self)

        self.radiusLayout: QHBoxLayout = QHBoxLayout()
        self.tlc = ComboBox(self)
        self.trc = ComboBox(self)
        self.brc = ComboBox(self)
        self.blc = ComboBox(self)

        self.tlc.addItems(self.radius)
        self.trc.addItems(self.radius)
        self.brc.addItems(self.radius)
        self.blc.addItems(self.radius)

        self.radiusLayout.addWidget(self.tlc)
        self.radiusLayout.addWidget(self.trc)
        self.radiusLayout.addWidget(self.brc)
        self.radiusLayout.addWidget(self.blc)

        self.applyButton: PrimaryPushButton = PrimaryPushButton("应用", self)

        self.viewLayout.addLayout(self.durationLayout)
        self.viewLayout.addLayout(self.clickOtherHideLayout)
        self.viewLayout.addWidget(self.radiusLabel, 1, Qt.AlignHCenter)
        self.viewLayout.addLayout(self.radiusLayout)
        self.viewLayout.addWidget(self.applyButton, 1, Qt.AlignHCenter)

        self.applyButton.clicked.connect(self.updateDrawer)

    def updateDrawer(self):
        try:
            duration = int(self.durationLineEdit.text())
        except ValueError:
            duration = 300
        clickedOtherHide = self.clickOterHideSwitchButton.isChecked()

        self.parent.leftPopupDrawer.setClickParentHide(clickedOtherHide)
        self.parent.topPopupDrawer.setClickParentHide(clickedOtherHide)
        self.parent.rightPopupDrawer.setClickParentHide(clickedOtherHide)
        self.parent.bottomPopupDrawer.setClickParentHide(clickedOtherHide)

        self.parent.leftPopupDrawer.setDuration(duration)
        self.parent.topPopupDrawer.setDuration(duration)
        self.parent.rightPopupDrawer.setDuration(duration)
        self.parent.bottomPopupDrawer.setDuration(duration)

        self.parent.leftPopupDrawer.setRoundRadius(
            int(self.tlc.currentText()), int(self.trc.currentText()), int(self.brc.currentText()), int(self.blc.currentText())
        )
        self.parent.topPopupDrawer.setRoundRadius(
            int(self.tlc.currentText()), int(self.trc.currentText()), int(self.brc.currentText()), int(self.blc.currentText())
        )
        self.parent.rightPopupDrawer.setRoundRadius(
            int(self.tlc.currentText()), int(self.trc.currentText()), int(self.brc.currentText()), int(self.blc.currentText())
        )
        self.parent.bottomPopupDrawer.setRoundRadius(
            int(self.tlc.currentText()), int(self.trc.currentText()), int(self.brc.currentText()), int(self.blc.currentText())
        )

        ToastInfoBar.success(
            "DrawerSetting",
            "所有设置应用成功!🥰",
            position=ToastInfoBarPosition.TOP,
            parent=self.parent
        )
        self.hide()


class DialogInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("对话框和弹出窗口", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("DialogInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.leftPopupDrawer: PopupDrawerWidget = PopupDrawerWidget("标题", parent=self)
        self.topPopupDrawer: PopupDrawerWidget = PopupDrawerWidget("标题", position=PopupDrawerPosition.TOP, parent=self)
        self.rightPopupDrawer: PopupDrawerWidget = PopupDrawerWidget("标题", position=PopupDrawerPosition.RIGHT, parent=self)
        self.bottomPopupDrawer: PopupDrawerWidget = PopupDrawerWidget("标题", position=PopupDrawerPosition.BOTTOM, parent=self)

        self.leftPopupDrawer.setClickParentHide(True)
        self.topPopupDrawer.setClickParentHide(True)
        self.rightPopupDrawer.setClickParentHide(True)
        self.bottomPopupDrawer.setClickParentHide(True)

        self.popLeftDrawerButton: PushButton = PushButton("左侧", self)
        self.popRightDrawerButton: PushButton = PushButton("右侧", self)
        self.popTopDrawerButton: PushButton = PushButton("顶侧", self)
        self.popBottomDrawerButton: PushButton = PushButton("底侧", self)
        self.popDrawerSettingButton: TransparentToolButton = TransparentToolButton(FluentIcon.SETTING, self)

        self.drawerSettingView: DrawerSettingView = DrawerSettingView(self.popDrawerSettingButton, self)

        layout.addWidget(self.popLeftDrawerButton)
        layout.addWidget(self.popRightDrawerButton)
        layout.addWidget(self.popTopDrawerButton)
        layout.addWidget(self.popBottomDrawerButton)
        layout.addWidget(self.popDrawerSettingButton, 1, Qt.AlignRight | Qt.AlignVCenter)
        self.addExamplesCard(
            "抽屉组件",
            widget,
            1
        ).widget.widgetCard.viewLayout.setContentsMargins(11, 11, 11, 11)

        self.addExamplesCard(
            "弹出调色盘",
            DropDownColorPalette(self)
        )

        self.addExamplesCard(
            "屏幕拾色器",
            ScreenColorPicker("deeppink", self)
        )

        self.targetButton: PushButton = PushButton("显示对话框", self)
        self.flyoutDialog: FlyoutDialog = FlyoutDialog(self.targetButton, parent=self)

        self.titleLabel: StrongBodyLabel = StrongBodyLabel("   无名", self)
        self.contentLabel: BodyLabel = BodyLabel("     左眼用来忘记你，右眼用来记住你。    ", self)
        self.yesBtn: TransparentToolButton = TransparentToolButton(FluentIcon.ACCEPT, self)
        self.closeBtn: TransparentToolButton = TransparentToolButton(FluentIcon.CLOSE, self)

        self.titleLabel.setFontSize(22)
        self.yesBtn.setFixedHeight(35)
        self.closeBtn.setFixedHeight(35)
        self.yesBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.closeBtn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.flyoutDialog.viewLayout.setContentsMargins(1, 10, 1, 0)
        self.flyoutDialog.viewLayout.addWidget(self.titleLabel)
        self.flyoutDialog.viewLayout.addSpacing(5)
        self.flyoutDialog.viewLayout.addWidget(self.contentLabel)
        self.flyoutDialog.viewLayout.addSpacing(10)
        self.flyoutDialog.viewLayout.addWidget(HorizontalSeparator(self))

        hBoxlayout = HBoxLayout()
        self.flyoutDialog.viewLayout.addLayout(hBoxlayout, 1)
        hBoxlayout.addWidget(self.yesBtn)
        hBoxlayout.addWidget(self.closeBtn)

        self.addExamplesCard(
            "弹出对话框",
            self.targetButton
        )

        self.scrollLayout.addStretch(1)
        self.connectSignalSlot()

    def connectSignalSlot(self):
        self.popLeftDrawerButton.clicked.connect(self.leftPopupDrawer.toggleDrawer)
        self.popTopDrawerButton.clicked.connect(self.topPopupDrawer.toggleDrawer)
        self.popRightDrawerButton.clicked.connect(self.rightPopupDrawer.toggleDrawer)
        self.popBottomDrawerButton.clicked.connect(self.bottomPopupDrawer.toggleDrawer)
        self.popDrawerSettingButton.clicked.connect(self.drawerSettingView.show)

        self.targetButton.clicked.connect(self.flyoutDialog.show)
        self.yesBtn.clicked.connect(self.flyoutDialog.hide)
        self.closeBtn.clicked.connect(self.flyoutDialog.hide)
