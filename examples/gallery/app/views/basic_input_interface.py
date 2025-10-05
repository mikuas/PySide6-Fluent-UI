# coding:utf-8
import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget

from PySide6FluentUI import FluentIcon, RoundPushButton, RoundToolButton, FillPushButton, FillToolButton, \
    OutlinePushButton, OutlineToolButton, LabelLineEdit, PinBox, MultiSelectionComboBox, \
    SubtitleRadioButton, ToolTipSlider

from ..widgets.basic_interface import Interface


class BasicInputInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("基本输入", "PySide6FluentUI.components.widgets", parent)
        self.setObjectName("BasicInputInterface")
        self.vBoxLayout.addWidget(self.scrollArea)

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

        """ outline push button """
        self.addExamplesCard(
            "描边按钮",
            OutlinePushButton(FluentIcon.VIDEO, "电影和电视", self)
        )

        """ outline tool button """
        self.addExamplesCard(
            "描边工具按钮",
            OutlineToolButton(FluentIcon.SETTING, self)
        )

        self.labelLineEdit: LabelLineEdit = LabelLineEdit("https://", ".com", self)
        self.labelLineEdit.setAlignment(Qt.AlignHCenter)
        self.addExamplesCard(
            "带前后缀的标签输入框",
            self.labelLineEdit
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