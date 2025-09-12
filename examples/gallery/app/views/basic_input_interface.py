# coding:utf-8
import json
from typing import List
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout

from PySide6FluentUI import FluentIcon, RoundPushButton, RoundToolButton, FillPushButton, FillToolButton, ComboBox, \
    OutlinePushButton, OutlineToolButton, LabelLineEdit, PinBox, MultiSelectionComboBox, PopupDrawerPosition, PopupDrawerWidget, \
    SubtitleRadioButton

from ..widgets.basic_interface import Interface
from ..widgets.widget_item import StandardItem


class BasicInputInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("基本输入", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("BasicInputInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

        self.__initButtonItem()
        self.__initLineEdit()
        self.__initComboBox()
        self.__initSubTitleRadio()

    def __initButtonItem(self):
        """ round push button """
        self.roundPushButtonItem: StandardItem = StandardItem("圆角按钮", self)
        self.roundPushButton: RoundPushButton = RoundPushButton(FluentIcon.ACCEPT, "圆角按钮", self)
        self.roundPushButtonItem.addWidget(self.roundPushButton)

        """ round tool button """        
        self.roundToolButtonItem: StandardItem = StandardItem("圆角工具按钮", self)
        self.roundToolButton: RoundToolButton = RoundToolButton(FluentIcon.GITHUB, self)
        self.roundToolButton.setFixedWidth(36)
        self.roundToolButtonItem.addWidget(self.roundToolButton)

        """ fill push button """
        self.fillPushButtonItem: StandardItem = StandardItem("填充按钮", self)
        self.fillPushButton: FillPushButton = FillPushButton(FluentIcon.HOME, "确定", self)
        self.fillPushButtonItem.addWidget(self.fillPushButton)

        """ fill tool button """
        self.fillToolButtonItem: StandardItem = StandardItem("填充工具按钮", self)
        self.fillToolButton: FillToolButton = FillToolButton(FluentIcon.HOME, self)
        self.fillToolButtonItem.addWidget(self.fillToolButton)

        """ outline push button """
        self.outlinePushButtonItem: StandardItem = StandardItem("描边按钮", self)
        self.outlinePushButton: OutlinePushButton = OutlinePushButton(FluentIcon.VIDEO, "电影和电视", self)
        self.outlinePushButtonItem.addWidget(self.outlinePushButton)

        """ outline tool button """
        self.outlineToolButtonItem: StandardItem = StandardItem("描边工具按钮", self)
        self.outlineToolButton: OutlineToolButton= OutlineToolButton(FluentIcon.SETTING, self)
        self.outlineToolButton.setFixedWidth(36)
        self.outlineToolButtonItem.addWidget(self.outlineToolButton)
        
        self.scrollLayout.addWidget(self.roundPushButtonItem)
        self.scrollLayout.addWidget(self.roundToolButtonItem)
        self.scrollLayout.addWidget(self.fillPushButtonItem)
        self.scrollLayout.addWidget(self.fillToolButtonItem)
        self.scrollLayout.addWidget(self.outlinePushButtonItem)
        self.scrollLayout.addWidget(self.outlineToolButtonItem)

    def __initLineEdit(self):
        self.labelLineEditItem: StandardItem = StandardItem("带前后缀的标签输入框", self)
        self.labelLineEdit: LabelLineEdit = LabelLineEdit("https://", ".com", self)
        self.labelLineEdit.setAlignment(Qt.AlignHCenter)
        self.labelLineEditItem.addWidget(self.labelLineEdit)
        
        self.pinBoxEditItem: StandardItem = StandardItem("PIN码输入框", self)
        self.pinBox: PinBox = PinBox(self)
        self.pinBoxEditItem.addWidget(self.pinBox, 1)
        
        self.scrollLayout.addWidget(self.labelLineEditItem)
        self.scrollLayout.addWidget(self.pinBoxEditItem)
        
    def __initComboBox(self):
        self.multiSelectionComboBoxItem: StandardItem = StandardItem("多选下拉框", self)
        self.multiSelectionComboBox: MultiSelectionComboBox = MultiSelectionComboBox(self, "Select You GirlFriend")
        self.multiSelectionComboBox.setFixedWidth(414)
        self.multiSelectionComboBoxItem.addWidget(self.multiSelectionComboBox)
        
        PATH = Path(__file__).resolve().parents[2] / "resources" / "json" / "data.json"
        with PATH.open("r", encoding="utf-8") as f:
            self.multiSelectionComboBox.addItems(json.load(f)["girlFriend"])
        self.scrollLayout.addWidget(self.multiSelectionComboBoxItem)

    def __initSubTitleRadio(self):
        self.subTitleRadioItem: StandardItem = StandardItem("带子标题的单选按钮", self)

        widgetLayout = QVBoxLayout()
        self.subTitleRadio1: SubtitleRadioButton = SubtitleRadioButton("扬声器", "Realtek(R) Audio", self)
        self.subTitleRadio2: SubtitleRadioButton = SubtitleRadioButton("耳机", "AirPods Pro 2", self)
        self.subTitleRadio3: SubtitleRadioButton = SubtitleRadioButton("控制器", "Xbox Wireless Controller", self)
        self.subTitleRadio4: SubtitleRadioButton = SubtitleRadioButton("蓝牙", "ProjectLuo M2", self)

        self.subTitleRadio4.setEnabled(False)

        widgetLayout.setContentsMargins(11, 15, 11, 15)
        widgetLayout.addWidget(self.subTitleRadio1)
        widgetLayout.addWidget(self.subTitleRadio2)
        widgetLayout.addWidget(self.subTitleRadio3)
        widgetLayout.addWidget(self.subTitleRadio4)

        self.subTitleRadioItem.card.setFixedHeight(264)
        self.subTitleRadioItem.addLayout(widgetLayout, 1)
        self.scrollLayout.addWidget(self.subTitleRadioItem)
    
    def initRoundSettingDrawer(self):
        self.roundSettingDrawer: PopupDrawerWidget = PopupDrawerWidget("Round Button Settings", position=PopupDrawerPosition.RIGHT, parent=self)
        
        self.radiusRange: List[str] = [str(_) for _ in range(6, 24)]
        self.radiusComboBox: ComboBox = ComboBox(self)
        self.radiusComboBox.addItems(self.radiusRange)