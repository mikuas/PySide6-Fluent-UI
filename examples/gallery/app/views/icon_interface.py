# coding:utf-8
import sys

from typing import List, Dict
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QSize, QRect, Signal
from PySide6.QtGui import QColor, QPainter, QIcon
from PySide6FluentUI import FluentIcon, FlowLayout, IconWidget as IW, BodyLabel, themeColor, isDarkTheme, CaptionLabel, \
    setFont, SmoothMode, SwitchButton, StrongBodyLabel
from PySide6FluentUI.common.icon import toQIcon

from ..widgets.basic_interface import Interface


class IconCard(QWidget):
    clicked = Signal(QWidget)

    def __init__(self, icon: FluentIcon, name: str, parent=None):
        super().__init__(parent)
        self.checked: bool = False
        self._icon = icon
        self._name: str = name
        self._data: Dict = {}
        setFont(self, 10)

    def mouseReleaseEvent(self, e):
        self.clicked.emit(self)

    def setChecked(self, checked: bool):
        if checked == self.checked:
            return
        self.checked = checked
        self.update()

    def isChecked(self):
        return self.checked

    def setData(self, data: Dict) -> None:
        self._data = data
    
    def data(self) -> Dict:
        return self._data
    
    def name(self) -> str:
        return self._name

    def icon(self) -> QIcon:
        return toQIcon(self._icon)
    
    def sizeHint(self) -> QSize:
        return QSize(100, 100)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(QColor(0, 0, 0, 32))
        isDark = isDarkTheme()
        if self.isChecked():
            self._icon = self._icon.colored(QColor(255, 255, 255), QColor(0, 0, 0))
            color = themeColor()
        else:
            self._icon = self._icon.colored(QColor(0, 0, 0), QColor(255, 255, 255))
            color = QColor("#2b2b2b") if isDark else QColor(255, 255, 255)
        painter.setBrush(color)
        
        rect = self.rect()
        painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 8, 8)
        self._drawIcon(painter)
        self._drawText(painter, rect)

    def _drawIcon(self, painter: QPainter) -> None:
        painter.setBrush(Qt.NoBrush)
        x = (self.width() - 32) / 2
        y = (self.height() - 32) / 2
        self._icon.render(painter, QRect(x, y, 32, 32))

    def _drawText(self, painter: QPainter, rect: QRect) -> None:
        if self.isChecked():
            c = 0 if isDarkTheme() else 255
        else:
            c = 255 if isDarkTheme() else 0
        painter.setPen(QColor(c, c, c))
        painter.drawText(rect.adjusted(0, 0, 0, -10), Qt.AlignBottom | Qt.AlignHCenter, self._name)


class IconInfoPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(145)
        self.vBoxLayout: QVBoxLayout = QVBoxLayout(self)
        self.titleLabel: BodyLabel = BodyLabel(self)
        self.iconWidget: IW = IW(self)
        self.nameTitle: BodyLabel = BodyLabel("图标名字", self)
        self.iconNameTitle: CaptionLabel = CaptionLabel(self)
        self.enumTitle: BodyLabel = BodyLabel("枚举成员", self)
        self.enumNameTitle: CaptionLabel = CaptionLabel(self)
        
        self.iconWidget.setFixedSize(64, 64)
        self.iconNameTitle.setTextColor(QColor("gray"), QColor("gray"))
        self.enumNameTitle.setTextColor(QColor("gray"), QColor("gray"))
        
        self.__initLayout()
        
    def __initLayout(self) -> None:
        self.vBoxLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.iconWidget)
        
        self.vBoxLayout.addSpacing(48)
        self.vBoxLayout.addWidget(self.nameTitle)
        self.vBoxLayout.addWidget(self.iconNameTitle)
        
        self.vBoxLayout.addSpacing(48)
        self.vBoxLayout.addWidget(self.enumTitle)
        self.vBoxLayout.addWidget(self.enumNameTitle)

    def setTitle(self, title: str) -> None:
        self.titleLabel.setText(title)
    
    def setIcon(self, icon: FluentIcon) -> None:
        self.iconWidget.setIcon(icon)
    
    def setIconName(self, name: str) -> None:
        self.iconNameTitle.setText(name)
    
    def setEnumName(self, name: str) -> None:
        self.enumNameTitle.setText(name)


class IconInterface(Interface):
    def __init__(self, parent=None):
        super().__init__("图标", "PySide6FluentUI.common.icon", parent)
        self.setObjectName("IconInterface")
        self.viewLayout: QHBoxLayout = QHBoxLayout()
        self.flowLayout: FlowLayout = FlowLayout()
        self.iconInfoPanel: IconInfoPanel = IconInfoPanel(self)

        hLayout: QHBoxLayout = QHBoxLayout()
        self.smoothLabel: StrongBodyLabel = StrongBodyLabel("启用平滑滚动", self)
        self.smoothSwitchButton: SwitchButton = SwitchButton(self)

        hLayout.addWidget(self.smoothLabel)
        hLayout.addSpacing(24)
        hLayout.addWidget(self.smoothSwitchButton)
        hLayout.setAlignment(Qt.AlignLeft)

        self.smoothSwitchButton.checkedChanged.connect(self._onSmoothModeChanged)
        self.vBoxLayout.addLayout(hLayout)

        self.vBoxLayout.addLayout(self.viewLayout)
        self.viewLayout.addWidget(self.scrollArea)
        self.viewLayout.setContentsMargins(0, 10, 0, 0)
        self.flowLayout.setContentsMargins(10, 10, 10, 5)
        self.scrollLayout.addLayout(self.flowLayout)

        self.cards: List[IconCard] = []
        self.icons: List[FluentIcon] = []
        self.names: List[str] = []

        self.icons = [icon for icon in list(FluentIcon)]
        self.names = [str(icon).split(".")[-1] for icon in self.icons]
        
        for icon, name in zip(self.icons, self.names):
            card = IconCard(icon, icon.value)
            card.setData({"name": icon.value, "icon": icon, "enum": f"FluentIcon.{name}"})
            card.clicked.connect(self._onClicked)
            self.cards.append(card)
            self.flowLayout.addWidget(card)

        self.viewLayout.addWidget(self.iconInfoPanel)

        self.updateBackgroundColor()
        self._onSmoothModeChanged(False)

    def update(self):
        self.updateBackgroundColor()
        super().update()
    
    def updateBackgroundColor(self):
        color = "#202020" if isDarkTheme() else "#f3f3f3"
        self.scrollArea.setStyleSheet(f"background: {color}; border-radius: 8px;")
    
    def _updateInfo(self, card: IconCard, update: bool) -> None:
        if update:
            data: Dict = card.data()
            self.iconInfoPanel.setTitle(data["name"])
            self.iconInfoPanel.setIcon(data["icon"])
            self.iconInfoPanel.setIconName(data["name"])
            self.iconInfoPanel.setEnumName(data["enum"])

    def _onClicked(self, card: IconCard):
        for c in self.cards:
            checked = c == card
            c.setChecked(checked)
            self._updateInfo(c, checked)

    def _onSmoothModeChanged(self, enable: bool):
        self.scrollArea.setSmoothMode(SmoothMode(1 if enable else 0), Qt.Vertical)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IconInterface()
    window.resize(810, 600)
    window.show()
    sys.exit(app.exec())