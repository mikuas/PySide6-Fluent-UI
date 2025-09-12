# coding:utf-8
from PySide6FluentUI import PopupDrawerWidget, PopupDrawerPosition, PushButton, DropDownColorPalette, ScreenColorPicker

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

    def connectSignalSlot(self):
        self.popLeftDrawerButton.clicked.connect(self.leftPopupDrawer.toggleDrawer)
        self.popTopDrawerButton.clicked.connect(self.topPopupDrawer.toggleDrawer)
        self.popRightDrawerButton.clicked.connect(self.rightPopupDrawer.toggleDrawer)
        self.popBottomDrawerButton.clicked.connect(self.bottomPopupDrawer.toggleDrawer)
