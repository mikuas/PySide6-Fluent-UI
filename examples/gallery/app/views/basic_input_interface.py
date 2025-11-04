# coding:utf-8
import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout

from PySide6FluentUI import FluentIcon, RoundPushButton, RoundToolButton, FillPushButton, FillToolButton, \
    OutlinePushButton, OutlineToolButton, LabelLineEdit, PinBox, MultiSelectionComboBox, SwitchButton, \
    SubtitleRadioButton, ToolTipSlider, PushButton, FocusLineEdit, TogglePushButton, HyperlinkButton, \
    PrimaryDropDownPushButton, RoundMenu, Action, PrimarySplitPushButton

from ..widgets.basic_interface import Interface


class BasicInputInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("基本输入", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("BasicInputInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

        """ push button """
        self.addExamplesCard(
            "标准按钮",
            PushButton(FluentIcon.HOME, "标准按钮", self)
        )

        """ toggle button """
        self.addExamplesCard(
            "切换按钮",
            TogglePushButton(FluentIcon.GITHUB, "切换按钮", self)
        )
        """ primary dropdown push button"""
        self.priDropDownPushButton: PrimaryDropDownPushButton = PrimaryDropDownPushButton("展开", self)
        self.priDropDownPushButtonMenu: RoundMenu = RoundMenu(parent=self)

        self.priDropDownPushButtonMenu.addActions([
            Action("打开", self),
            Action(FluentIcon.SAVE, "保存", self),
            Action(FluentIcon.SAVE_AS, "另存为", self),
            Action(FluentIcon.CLOSE, "关闭", self),
        ])
        self.priDropDownPushButton.setMenu(self.priDropDownPushButtonMenu)
        self.priDropDownPushButton.setMinimumWidth(128)
        self.addExamplesCard(
            "主题色下拉按钮",
            self.priDropDownPushButton
        )

        """ primary split push button """
        self.priSplitPushButton: PrimarySplitPushButton = PrimarySplitPushButton(FluentIcon.PLAY, "播放", self)
        self.priSplitPushButton.setFlyout(self.priDropDownPushButtonMenu)
        self.addExamplesCard(
            "主题色分割按钮",
            self.priSplitPushButton
        )

        """ hyperlink button """
        self.addExamplesCard(
            "超链接按钮",
            HyperlinkButton("", "我是超链接按钮", self, FluentIcon.LINK)
        )

        """ round push button """
        self.addExamplesCard(
            "圆角按钮",
            RoundPushButton(FluentIcon.ACCEPT, "圆角按钮", self)
        )

        """ round tool button """
        self.addExamplesCard(
            "圆角工具按钮",
            RoundToolButton(FluentIcon.GITHUB, self)
        )
        # self.roundToolButton.setFixedWidth(36)

        """ fill push button """
        self.addExamplesCard(
            "填充按钮",
            FillPushButton(FluentIcon.HOME, "确定", self)
        )

        """ fill tool button """
        self.addExamplesCard(
            "填充工具按钮",
            FillToolButton(FluentIcon.HOME, self)
        )

        """ switch button """
        self.addExamplesCard(
            "开关按钮",
            SwitchButton(self)
        )

        """ outline push button """
        widget = QWidget()
        widget.setLayout(QHBoxLayout())
        widget.layout().setContentsMargins(0, 0, 0, 0)
        widget.layout().addWidget(OutlinePushButton(FluentIcon.MUSIC, "音乐", self))
        widget.layout().addWidget(OutlinePushButton(FluentIcon.VIDEO, "电影和电视", self))
        widget.layout().addWidget(OutlinePushButton(FluentIcon.GAME, "游戏", self))
        widget.layout().addWidget(OutlinePushButton(FluentIcon.GITHUB, "GitHub", self))
        widget.layout().addWidget(OutlinePushButton("关于我们", self))
        self.addExamplesCard(
            "描边按钮",
            widget
        )

        """ outline tool button """
        self.addExamplesCard(
            "描边工具按钮",
            OutlineToolButton(FluentIcon.SETTING, self)
        )

        self.labelLineEdit: LabelLineEdit = LabelLineEdit("https://", ".com", self)
        self.labelLineEdit.setClearButtonEnabled(True)
        self.labelLineEdit.setAlignment(Qt.AlignHCenter)
        self.addExamplesCard(
            "带前后缀的标签输入框",
            self.labelLineEdit
        )

        self.focusLineEdit: FocusLineEdit = FocusLineEdit(self)
        self.focusLineEdit.setClearButtonEnabled(True)
        self.focusLineEdit.setMinimumWidth(256)
        self.addExamplesCard(
            "焦点输入框",
            self.focusLineEdit
        )

        self.addExamplesCard(
            "PIN码输入框",
            PinBox(self)
        )

        self.multiSelectionComboBox: MultiSelectionComboBox = MultiSelectionComboBox(self, "Select You GirlFriend")
        self.multiSelectionComboBox.setFixedWidth(414)

        PATH = Path(__file__).resolve().parents[2] / "resources" / "json" / "data.json"
        with PATH.open("r", encoding="utf-8") as f:
            self.multiSelectionComboBox.addItems(json.load(f)["girlFriend"])
        self.addExamplesCard(
            "多选下拉框",
            self.multiSelectionComboBox
        )

        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        self.subTitleRadio1: SubtitleRadioButton = SubtitleRadioButton("扬声器", "Realtek(R) Audio", self)
        self.subTitleRadio2: SubtitleRadioButton = SubtitleRadioButton("耳机", "AirPods Pro 2", self)
        self.subTitleRadio3: SubtitleRadioButton = SubtitleRadioButton("控制器", "Xbox Wireless Controller", self)
        self.subTitleRadio4: SubtitleRadioButton = SubtitleRadioButton("蓝牙", "ProjectLuo M2", self)

        self.subTitleRadio4.setEnabled(False)

        widget.layout().setContentsMargins(11, 15, 11, 15)
        widget.layout().addWidget(self.subTitleRadio1)
        widget.layout().addWidget(self.subTitleRadio2)
        widget.layout().addWidget(self.subTitleRadio3)
        widget.layout().addWidget(self.subTitleRadio4)
        self.addExamplesCard(
            "带子标题的单选按钮",
            widget,
            1
        )

        self.toolTipSlider: ToolTipSlider = ToolTipSlider(Qt.Orientation.Horizontal, self)
        self.toolTipSlider.setRange(0, 100)
        self.toolTipSlider.setFixedWidth(256)
        self.addExamplesCard(
            "带工具提示的滑动条",
            self.toolTipSlider
        )

        self.scrollLayout.addStretch(1)