# coding:utf-8
from PySide6.QtWidgets import QSizePolicy

from PySide6FluentUI import PopupDrawerWidget, PopupDrawerPosition, PushButton, DropDownColorPalette, ScreenColorPicker, \
    FlyoutDialog, StrongBodyLabel, BodyLabel, TransparentToolButton, FluentIcon, HorizontalSeparator, HBoxLayout

from ..widgets.basic_interface import Interface
from ..widgets.widget_item import StandardItem


class DialogInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("对话框和弹出窗口", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("DialogInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

        self.__initPopupDrawer()
        self.__initDropDownColorPalette()
        self.__initScreenColorPicker()
        self.__initFlyoutDialog()
        self.scrollLayout.addStretch(1)
        self.connectSignalSlot()

    def __initPopupDrawer(self):
        self.popupDrawerItem: StandardItem = StandardItem("抽屉组件", self)
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

        self.popupDrawerItem.addWidget(self.popLeftDrawerButton)
        self.popupDrawerItem.addWidget(self.popRightDrawerButton)
        self.popupDrawerItem.addWidget(self.popTopDrawerButton)
        self.popupDrawerItem.addWidget(self.popBottomDrawerButton)

        self.scrollLayout.addWidget(self.popupDrawerItem)

    def __initDropDownColorPalette(self):
        self.colorPaletteItem: StandardItem = StandardItem("弹出调色盘", self)
        self.colorPalette: DropDownColorPalette = DropDownColorPalette(self)

        self.colorPaletteItem.addWidget(self.colorPalette)
        self.scrollLayout.addWidget(self.colorPaletteItem)

    def __initScreenColorPicker(self):
        self.screenColorItem: StandardItem = StandardItem("屏幕拾色器", self)
        self.screenColorPicker: ScreenColorPicker = ScreenColorPicker(self)

        self.screenColorItem.addWidget(self.screenColorPicker)
        self.scrollLayout.addWidget(self.screenColorItem)

    def __initFlyoutDialog(self):
        self.flyoutDialogItem: StandardItem = StandardItem("弹出对话框", self)
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

        self.flyoutDialogItem.addWidget(self.targetButton)
        self.scrollLayout.addWidget(self.flyoutDialogItem)

    def connectSignalSlot(self):
        self.popLeftDrawerButton.clicked.connect(self.leftPopupDrawer.toggleDrawer)
        self.popTopDrawerButton.clicked.connect(self.topPopupDrawer.toggleDrawer)
        self.popRightDrawerButton.clicked.connect(self.rightPopupDrawer.toggleDrawer)
        self.popBottomDrawerButton.clicked.connect(self.bottomPopupDrawer.toggleDrawer)
        self.targetButton.clicked.connect(self.flyoutDialog.show)
        self.yesBtn.clicked.connect(self.flyoutDialog.hide)
        self.closeBtn.clicked.connect(self.flyoutDialog.hide)
