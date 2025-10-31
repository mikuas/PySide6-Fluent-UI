# coding:utf-8
from PySide6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt, QStringListModel

from PySide6FluentUI import FlyoutDialog, SubtitleLabel, PrimaryPushButton, FocusLineEdit, PopupDrawerWidget, \
    SingleDirectionScrollArea, RoundListWidget, FlyoutPosition, CaptionLabel, ComboBox


class RadiusView(FlyoutDialog):
    def __init__(self, target, parent=None):
        super().__init__(target, FlyoutPosition.RIGHT, parent)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)
        self.viewLayout.setSpacing(12)

        self.tlEdit: FocusLineEdit = FocusLineEdit(self)
        self.trEdit: FocusLineEdit = FocusLineEdit(self)
        self.brEdit: FocusLineEdit = FocusLineEdit(self)
        self.blEdit: FocusLineEdit = FocusLineEdit(self)

        self.intValidator: QIntValidator = QIntValidator(0, 999, self)
        for edit, text, in zip([self.tlEdit, self.trEdit, self.brEdit, self.blEdit], ["左上角", "右上角", "右下角", "左下角"]):
            edit.setValidator(self.intValidator)
            edit.setPlaceholderText(text)
        self.radiusLabel: SubtitleLabel = SubtitleLabel("设置圆角弧度(左上, 右上, 右下, 左下)", self)
        self.applyButton: PrimaryPushButton = PrimaryPushButton("应用", self)

        self.viewLayout.addWidget(self.radiusLabel, 1, Qt.AlignHCenter)

        hBoxLayout: QHBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(self.tlEdit)
        hBoxLayout.addWidget(self.trEdit)
        hBoxLayout.addWidget(self.brEdit)
        hBoxLayout.addWidget(self.blEdit)
        self.viewLayout.addLayout(hBoxLayout)
        self.viewLayout.addWidget(self.applyButton)

    def getRadius(self):
        try:
            return int(self.tlEdit.text()), int(self.trEdit.text()), int(self.brEdit.text()), int(self.blEdit.text())
        except ValueError:
            return 0, 0, 0, 0


class OptionView(PopupDrawerWidget):
    def __init__(self, parent=None):
        super().__init__("选项", parent=parent)
        self.setClickParentHide(True)
        self.imageListLabel: SubtitleLabel = SubtitleLabel("图片列表 目录:", self)
        self.setRadiusButton: PrimaryPushButton = PrimaryPushButton("设置圆角弧度", self)
        self.radiusView: RadiusView = RadiusView(self.setRadiusButton, self)
        self.saveTypeLabel: SubtitleLabel = SubtitleLabel("保存类型", self)
        self.saveTypeComboBox: ComboBox = ComboBox(self)

        self.imageListLabel.setFontSize(18)
        self.imageListLabel.setAlignment(Qt.AlignHCenter)
        self.imageListLabel.setWordWrap(True)
        self.saveTypeLabel.setFontSize(18)
        self.saveTypeLabel.setContentsMargins(0, 12, 0, 12)
        self.saveTypes: list[str] = ["png", "webp"]
        self.saveTypeComboBox.addItems(["png(体积大)", "webp(体积小)"])

        self.roundListWidget: RoundListWidget = RoundListWidget(self)
        self.roundListWidget.setMinimumHeight(266)
        # self.roundListWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.viewLayout.addWidget(self.imageListLabel, 0, Qt.AlignHCenter)
        self.viewLayout.addWidget(self.roundListWidget, 1)
        self.viewLayout.addWidget(self.setRadiusButton)
        self.viewLayout.addWidget(self.saveTypeLabel, 0, Qt.AlignHCenter)
        self.viewLayout.addWidget(self.saveTypeComboBox)

        self.connectSignalSlot()

    def connectSignalSlot(self):
        self.setRadiusButton.clicked.connect(self.radiusView.show)