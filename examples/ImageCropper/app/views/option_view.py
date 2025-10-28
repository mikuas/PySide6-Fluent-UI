# coding:utf-8
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt

from PySide6FluentUI import FlyoutDialog, EditableComboBox, SubtitleLabel, PrimaryPushButton


class OptionView(FlyoutDialog):
    def __init__(self, target, parent=None):
        super().__init__(target, parent=parent)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)
        self.viewLayout.setSpacing(12)

        self.tl, self.tr, self.br, self.bl = 0, 0, 0, 0
        self.tlc: EditableComboBox = EditableComboBox(self)
        self.trc: EditableComboBox = EditableComboBox(self)
        self.brc: EditableComboBox = EditableComboBox(self)
        self.blc: EditableComboBox = EditableComboBox(self)

        self.intValidator: QIntValidator = QIntValidator(self)

        radius: list[str] = [str(r * 8) for r in range(0, 25)]
        self.comboBoxs = [self.tlc, self.trc, self.brc, self.blc]
        for c in self.comboBoxs:
            c.setValidator(self.intValidator)
            c.addItems(radius)
            c.setCurrentText("64")

        self.radiusLabel: SubtitleLabel = SubtitleLabel("设置圆角弧度(左上, 右上, 右下, 左下)", self)
        self.applyButton: PrimaryPushButton = PrimaryPushButton("应用", self)

        self.viewLayout.addWidget(self.radiusLabel, 1, Qt.AlignHCenter)

        hBoxLayout: QHBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(self.tlc)
        hBoxLayout.addWidget(self.trc)
        hBoxLayout.addWidget(self.brc)
        hBoxLayout.addWidget(self.blc)
        self.viewLayout.addLayout(hBoxLayout)
        self.viewLayout.addWidget(self.applyButton)

    def getRadius(self):
        return int(self.tlc.currentText()), int(self.trc.currentText()), int(self.brc.currentText()), int(self.blc.currentText())