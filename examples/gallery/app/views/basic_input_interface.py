# coding:utf-8
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
        widget = QWidget()
        widget.setLayout(QHBoxLayout())
        widget.layout().setContentsMargins(0, 0, 0, 0)
        self.roundPushButton1: RoundPushButton = RoundPushButton(FluentIcon.ACCEPT, "圆角按钮", self)
        self.roundPushButton2: RoundPushButton = RoundPushButton("圆角按钮(radius: 8)", self)
        self.roundPushButton2.setRadius(8, 8, 8, 8)
        widget.layout().addWidget(self.roundPushButton1)
        widget.layout().addWidget(self.roundPushButton2)
        self.addExamplesCard(
            "圆角按钮",
            widget
        )

        """ round tool button """
        self.addExamplesCard(
            "圆角工具按钮",
            RoundToolButton(FluentIcon.GITHUB, self)
        )
        # self.roundToolButton.setFixedWidth(36)

        """ fill push button """
        widget = QWidget()
        widget.setLayout(QHBoxLayout())
        widget.layout().setContentsMargins(0, 0, 0, 0)

        self.fillPushButton1: FillPushButton = FillPushButton(FluentIcon.ACCEPT, "确定", self)
        self.fillPushButton2: FillPushButton = FillPushButton(FluentIcon.CLOSE, "取消", self)
        self.fillPushButton3: FillPushButton = FillPushButton(FluentIcon.SETTING, "设置", self)

        self.fillPushButton2.setFillColor("#8fda69")
        self.fillPushButton2.setTextColor("#fb8500", "#9d4edd")
        self.fillPushButton3.setFillColor("#ff8081")
        widget.layout().addWidget(self.fillPushButton1)
        widget.layout().addWidget(self.fillPushButton2)
        widget.layout().addWidget(self.fillPushButton3)

        self.addExamplesCard(
            "填充按钮",
            widget
        )

        widget = QWidget()
        widget.setLayout(QHBoxLayout())
        widget.layout().setContentsMargins(0, 0, 0, 0)

        self.fillToolButton1: FillToolButton = FillToolButton(FluentIcon.HOME, self)
        self.fillToolButton2: FillToolButton = FillToolButton(FluentIcon.GITHUB, self)
        self.fillToolButton3: FillToolButton = FillToolButton(FluentIcon.VIDEO, self)
        self.fillToolButton4: FillToolButton = FillToolButton(FluentIcon.SETTING, self)

        self.fillToolButton2.setFillColor("#8fda69")
        self.fillToolButton2.setTextColor("#fb8500", "#9d4edd")
        self.fillToolButton3.setFillColor("#ff8081")
        self.fillToolButton4.setFillColor("#9d9d9d")
        widget.layout().addWidget(self.fillToolButton1)
        widget.layout().addWidget(self.fillToolButton2)
        widget.layout().addWidget(self.fillToolButton3)
        widget.layout().addWidget(self.fillToolButton4)
        """ fill tool button """
        self.addExamplesCard(
            "填充工具按钮",
            widget
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

        # widget = QWidget()
        # widget.setLayout(QVBoxLayout())
        # self.userNameMotionLineEdit: MotionLineEdit = MotionLineEdit("用户名", self)
        # self.passwdMotionLineEdit: MotionLineEdit = MotionLineEdit("密码", self)
        # self.phoneMotionLineEdit: MotionLineEdit = MotionLineEdit("手机号码", self)
        # self.emailMotionLineEdit: MotionLineEdit = MotionLineEdit("邮箱地址", self)
        #
        # self.userNameMotionLineEdit.setPlaceholderText("请输入用户名")
        # self.passwdMotionLineEdit.setPlaceholderText("密码至少包含一位大写,小写字母,特殊符号及数字")
        # self.phoneMotionLineEdit.setPlaceholderText("请输入11位手机号")
        # self.emailMotionLineEdit.setPlaceholderText("请输入邮箱地址")
        # self.userNameMotionLineEdit.setFixedWidth(328)
        # self.passwdMotionLineEdit.setFixedWidth(328)
        # self.phoneMotionLineEdit.setFixedWidth(328)
        # self.emailMotionLineEdit.setFixedWidth(328)
        # widget.layout().setContentsMargins(12, 12, 12, 12)
        # widget.layout().addWidget(self.userNameMotionLineEdit)
        # widget.layout().addWidget(self.passwdMotionLineEdit)
        # widget.layout().addWidget(self.phoneMotionLineEdit)
        # widget.layout().addWidget(self.emailMotionLineEdit)
        # self.addExamplesCard(
        #     "动态线编辑框",
        #     widget,
        #     1
        # )

        self.addExamplesCard(
            "PIN码输入框",
            PinBox(self)
        )

        self.multiSelectionComboBox: MultiSelectionComboBox = MultiSelectionComboBox(self, "Select You GirlFriend")
        self.multiSelectionComboBox.setFixedWidth(414)

        self.multiSelectionComboBox.addItems([
                "绫地宁宁",
                "因幡爱瑠",
                "椎叶䌷",
                "亚托莉",
                "朝武芳乃",
                "丛雨",
                "常陆茉子",
                "上坂茅羽耶",
                "矢来美羽",
                "在原七海",
                "三司绫濑",
                "式部茉优",
                "二条院羽月",
                "和泉妃爱",
                "常盘华乃",
                "镰仓诗樱",
                "结城明日奈",
                "小鸟游六花",
                "御坂美琴",
                "佐天泪子",
                "后藤一里",
                "山田凉",
                "伊地知虹夏",
                "喜多郁代",
                "锦亚澄",
                "圣莉莉子"
        ])
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