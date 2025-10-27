# coding:utf-8
import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor, QIntValidator
from PySide6.QtCore import Qt

from PySide6FluentUI import FlyoutDialog, EditableComboBox, SubtitleLabel


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

        self.tlc.setValidator(self.intValidator)
        self.trc.setValidator(self.intValidator)
        self.brc.setValidator(self.intValidator)
        self.blc.setValidator(self.intValidator)

        self.radius: list[str] = [str(r) for r in range(0, 25)]

        self.tlc.addItems(self.radius)
        self.trc.addItems(self.radius)
        self.brc.addItems(self.radius)
        self.blc.addItems(self.radius)

        self.radiusLabel: SubtitleLabel = SubtitleLabel("设置圆角弧度(左上, 右上, 右下, 左下)", self)

        self.viewLayout.addWidget(self.radiusLabel)

        hBoxLayout: QHBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(self.tlc)
        hBoxLayout.addWidget(self.trc)
        hBoxLayout.addWidget(self.brc)
        hBoxLayout.addWidget(self.blc)
        self.viewLayout.addLayout(hBoxLayout)

    def getRadius(self) -> list[int]:
        return [
            int(self.tlc.currentText()), int(self.trc.currentText()), int(self.brc.currentText()), int(self.blc.currentText())
        ]