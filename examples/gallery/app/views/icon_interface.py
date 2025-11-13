# coding:utf-8
import sys

from typing import List
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt, Signal
from PySide6FluentUI import FluentIcon, FlowLayout, isDarkTheme, StrongBodyLabel, SearchLineEdit, IconWidget, \
    Theme, SmoothScrollArea

from ..widgets.basic_interface import Interface
from ..common.trie import Trie
from ..common.config import cfg
from ..common.style_sheet import StyleSheet


class LineEdit(SearchLineEdit):
    """ Search line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("搜索图标")
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)


class IconCard(QFrame):
    """ Icon card """

    clicked = Signal(FluentIcon)

    def __init__(self, icon: FluentIcon, parent=None):
        super().__init__(parent=parent)
        self.icon = icon
        self.isSelected = False

        self.iconWidget = IconWidget(icon, self)
        self.nameLabel = QLabel(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.setFixedSize(96, 96)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(8, 28, 8, 0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.iconWidget.setFixedSize(28, 28)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignHCenter)
        self.vBoxLayout.addSpacing(14)
        self.vBoxLayout.addWidget(self.nameLabel, 0, Qt.AlignHCenter)

        text = self.nameLabel.fontMetrics().elidedText(icon.value, Qt.ElideRight, 90)
        self.nameLabel.setText(text)

    def mouseReleaseEvent(self, e):
        if self.isSelected:
            return

        self.clicked.emit(self.icon)

    def setSelected(self, isSelected: bool, force=False):
        if isSelected == self.isSelected and not force:
            return

        self.isSelected = isSelected

        if not isSelected:
            self.iconWidget.setIcon(self.icon)
        else:
            icon = self.icon.icon(Theme.LIGHT if isDarkTheme() else Theme.DARK)
            self.iconWidget.setIcon(icon)

        self.setProperty('isSelected', isSelected)
        self.setStyle(QApplication.style())


class IconInfoPanel(QFrame):
    """ Icon info panel """

    def __init__(self, icon: FluentIcon, parent=None):
        super().__init__(parent=parent)
        self.nameLabel = QLabel(icon.value, self)
        self.iconWidget = IconWidget(icon, self)
        self.iconNameTitleLabel = QLabel(self.tr('Icon name'), self)
        self.iconNameLabel = QLabel(icon.value, self)
        self.enumNameTitleLabel = QLabel(self.tr('Enum member'), self)
        self.enumNameLabel = QLabel("FluentIcon." + icon.name, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(16, 20, 16, 20)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.vBoxLayout.addWidget(self.nameLabel)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(45)
        self.vBoxLayout.addWidget(self.iconNameTitleLabel)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.iconNameLabel)
        self.vBoxLayout.addSpacing(34)
        self.vBoxLayout.addWidget(self.enumNameTitleLabel)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.enumNameLabel)

        self.iconWidget.setFixedSize(48, 48)
        self.setFixedWidth(216)

        self.nameLabel.setObjectName('nameLabel')
        self.iconNameTitleLabel.setObjectName('subTitleLabel')
        self.enumNameTitleLabel.setObjectName('subTitleLabel')

    def setIcon(self, icon: FluentIcon):
        self.iconWidget.setIcon(icon)
        self.nameLabel.setText(icon.value)
        self.iconNameLabel.setText(icon.value)
        self.enumNameLabel.setText("FluentIcon."+icon.name)


class IconCardView(QWidget):
    """ Icon card view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.trie = Trie()
        self.iconLibraryLabel = StrongBodyLabel('Fluent 图标库', self)
        self.searchLineEdit = LineEdit(self)

        self.view = QFrame(self)
        self.scrollArea = SmoothScrollArea(self.view)
        self.scrollWidget = QWidget(self.scrollArea)
        self.infoPanel = IconInfoPanel(FluentIcon.MENU, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.flowLayout = FlowLayout(self.scrollWidget, isTight=True)

        self.cards = []     # type:List[IconCard]
        self.icons = []
        self.currentIndex = -1

        self.__initWidget()

    def __initWidget(self):
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.enableTransparentBackground()
        self.scrollArea.setViewportMargins(6, 10, 10, 10)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.addWidget(self.iconLibraryLabel)
        self.vBoxLayout.addWidget(self.searchLineEdit)
        self.vBoxLayout.addWidget(self.view)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.scrollArea)
        self.hBoxLayout.addWidget(self.infoPanel, 0, Qt.AlignRight)

        self.flowLayout.setVerticalSpacing(8)
        self.flowLayout.setHorizontalSpacing(8)
        self.flowLayout.setContentsMargins(8, 3, 8, 8)

        self.__setQss()
        cfg.themeChanged.connect(self.__setQss)
        self.searchLineEdit.clearSignal.connect(self.showAllIcons)
        self.searchLineEdit.searchSignal.connect(self.search)

        for icon in FluentIcon._member_map_.values():
            self.addIcon(icon)

        self.setSelectedIcon(self.icons[0])

    def addIcon(self, icon: FluentIcon):
        """ add icon to view """
        card = IconCard(icon, self)
        card.clicked.connect(self.setSelectedIcon)

        self.trie.insert(icon.value, len(self.cards))
        self.cards.append(card)
        self.icons.append(icon)
        self.flowLayout.addWidget(card)

    def setSelectedIcon(self, icon: FluentIcon):
        """ set selected icon """
        index = self.icons.index(icon)

        if self.currentIndex >= 0:
            self.cards[self.currentIndex].setSelected(False)

        self.currentIndex = index
        self.cards[index].setSelected(True)
        self.infoPanel.setIcon(icon)

    def __setQss(self):
        self.view.setObjectName('iconView')
        self.scrollWidget.setObjectName('scrollWidget')

        StyleSheet.ICON_INTERFACE.apply(self)
        StyleSheet.ICON_INTERFACE.apply(self.scrollWidget)

        if self.currentIndex >= 0:
            self.cards[self.currentIndex].setSelected(True, True)

    def search(self, keyWord: str):
        """ search icons """
        items = self.trie.items(keyWord.lower())
        indexes = {i[1] for i in items}
        self.flowLayout.removeAllWidgets()

        for i, card in enumerate(self.cards):
            isVisible = i in indexes
            card.setVisible(isVisible)
            if isVisible:
                self.flowLayout.addWidget(card)

    def showAllIcons(self):
        self.flowLayout.removeAllWidgets()
        for card in self.cards:
            card.show()
            self.flowLayout.addWidget(card)


class IconInterface(Interface):
    """ Icon interface """

    def __init__(self, parent=None):
        super().__init__("图标", "PySide6FluentUI.common.icon", parent)
        self.setObjectName('iconInterface')
        self.iconView = IconCardView(self)
        self.scrollArea.deleteLater()
        self.vBoxLayout.addWidget(self.iconView)


# class IconCard(QWidget):
#     clicked = Signal(QWidget)
#
#     def __init__(self, icon: FluentIcon, name: str, parent=None):
#         super().__init__(parent)
#         self.checked: bool = False
#         self._icon = icon
#         self._name: str = name
#         self._data: Dict = {}
#         setFont(self, 10)
#
#     def mouseReleaseEvent(self, e):
#         self.clicked.emit(self)
#
#     def setChecked(self, checked: bool):
#         if checked == self.checked:
#             return
#         self.checked = checked
#         self.update()
#
#     def isChecked(self):
#         return self.checked
#
#     def setData(self, data: Dict) -> None:
#         self._data = data
#
#     def data(self) -> Dict:
#         return self._data
#
#     def name(self) -> str:
#         return self._name
#
#     def icon(self) -> QIcon:
#         return toQIcon(self._icon)
#
#     def sizeHint(self) -> QSize:
#         return QSize(100, 100)
#
#     def paintEvent(self, e) -> None:
#         painter = QPainter(self)
#         painter.setRenderHints(QPainter.RenderHint.Antialiasing)
#         painter.setPen(QColor(0, 0, 0, 32))
#         isDark = isDarkTheme()
#         if self.isChecked():
#             self._icon = self._icon.colored(QColor(255, 255, 255), QColor(0, 0, 0))
#             color = themeColor()
#         else:
#             self._icon = self._icon.colored(QColor(0, 0, 0), QColor(255, 255, 255))
#             color = QColor("#2b2b2b") if isDark else QColor(255, 255, 255)
#         painter.setBrush(color)
#
#         rect = self.rect()
#         painter.drawRoundedRect(rect.adjusted(1, 1, -1, -1), 8, 8)
#         self._drawIcon(painter)
#         self._drawText(painter, rect)
#
#     def _drawIcon(self, painter: QPainter) -> None:
#         painter.setBrush(Qt.NoBrush)
#         x = (self.width() - 32) / 2
#         y = (self.height() - 32) / 2
#         self._icon.render(painter, QRect(x, y, 32, 32))
#
#     def _drawText(self, painter: QPainter, rect: QRect) -> None:
#         if self.isChecked():
#             c = 0 if isDarkTheme() else 255
#         else:
#             c = 255 if isDarkTheme() else 0
#         painter.setPen(QColor(c, c, c))
#         painter.drawText(rect.adjusted(0, 0, 0, -10), Qt.AlignBottom | Qt.AlignHCenter, self._name)
#
#
# class IconInfoPanel(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setFixedWidth(145)
#         self.vBoxLayout: QVBoxLayout = QVBoxLayout(self)
#         self.titleLabel: BodyLabel = BodyLabel(self)
#         self.iconWidget: IW = IW(self)
#         self.nameTitle: BodyLabel = BodyLabel("图标名字", self)
#         self.iconNameTitle: CaptionLabel = CaptionLabel(self)
#         self.enumTitle: BodyLabel = BodyLabel("枚举成员", self)
#         self.enumNameTitle: CaptionLabel = CaptionLabel(self)
#
#         self.iconWidget.setFixedSize(64, 64)
#         self.iconNameTitle.setTextColor(QColor("gray"), QColor("gray"))
#         self.enumNameTitle.setTextColor(QColor("gray"), QColor("gray"))
#
#         self.__initLayout()
#
#     def __initLayout(self) -> None:
#         self.vBoxLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
#         self.vBoxLayout.addWidget(self.titleLabel)
#         self.vBoxLayout.addWidget(self.iconWidget)
#
#         self.vBoxLayout.addSpacing(48)
#         self.vBoxLayout.addWidget(self.nameTitle)
#         self.vBoxLayout.addWidget(self.iconNameTitle)
#
#         self.vBoxLayout.addSpacing(48)
#         self.vBoxLayout.addWidget(self.enumTitle)
#         self.vBoxLayout.addWidget(self.enumNameTitle)
#
#     def setTitle(self, title: str) -> None:
#         self.titleLabel.setText(title)
#
#     def setIcon(self, icon: FluentIcon) -> None:
#         self.iconWidget.setIcon(icon)
#
#     def setIconName(self, name: str) -> None:
#         self.iconNameTitle.setText(name)
#
#     def setEnumName(self, name: str) -> None:
#         self.enumNameTitle.setText(name)
#
#
# class IconInterface(Interface):
#     def __init__(self, parent=None):
#         super().__init__("图标", "PySide6FluentUI.common.icon", parent)
#         self.setObjectName("IconInterface")
#         self.viewLayout: QHBoxLayout = QHBoxLayout()
#         self.flowLayout: FlowLayout = FlowLayout()
#         self.iconInfoPanel: IconInfoPanel = IconInfoPanel(self)
#
#         hLayout: QHBoxLayout = QHBoxLayout()
#         self.smoothLabel: StrongBodyLabel = StrongBodyLabel("启用平滑滚动", self)
#         self.smoothSwitchButton: SwitchButton = SwitchButton(self)
#
#         hLayout.addWidget(self.smoothLabel)
#         hLayout.addSpacing(24)
#         hLayout.addWidget(self.smoothSwitchButton)
#         hLayout.setAlignment(Qt.AlignLeft)
#
#         self.smoothSwitchButton.checkedChanged.connect(self._onSmoothModeChanged)
#         self.vBoxLayout.addLayout(hLayout)
#
#         self.vBoxLayout.addLayout(self.viewLayout)
#         self.viewLayout.addWidget(self.scrollArea)
#         self.viewLayout.setContentsMargins(0, 10, 0, 0)
#         self.flowLayout.setContentsMargins(10, 10, 10, 5)
#         self.scrollLayout.addLayout(self.flowLayout)
#
#         self.cards: List[IconCard] = []
#         self.icons: List[FluentIcon] = []
#         self.names: List[str] = []
#
#         self.icons = [icon for icon in list(FluentIcon)]
#         self.names = [str(icon).split(".")[-1] for icon in self.icons]
#
#         for icon, name in zip(self.icons, self.names):
#             card = IconCard(icon, icon.value)
#             card.setData({"name": icon.value, "icon": icon, "enum": f"FluentIcon.{name}"})
#             card.clicked.connect(self._onClicked)
#             self.cards.append(card)
#             self.flowLayout.addWidget(card)
#
#         self.viewLayout.addWidget(self.iconInfoPanel)
#
#         self.updateBackgroundColor()
#         self._onSmoothModeChanged(False)
#
#     def update(self):
#         self.updateBackgroundColor()
#         super().update()
#
#     def updateBackgroundColor(self):
#         color = "#202020" if isDarkTheme() else "#f3f3f3"
#         self.scrollArea.setStyleSheet(f"background: {color}; border-radius: 8px;")
#
#     def _updateInfo(self, card: IconCard, update: bool) -> None:
#         if update:
#             data: Dict = card.data()
#             self.iconInfoPanel.setTitle(data["name"])
#             self.iconInfoPanel.setIcon(data["icon"])
#             self.iconInfoPanel.setIconName(data["name"])
#             self.iconInfoPanel.setEnumName(data["enum"])
#
#     def _onClicked(self, card: IconCard):
#         for c in self.cards:
#             checked = c == card
#             c.setChecked(checked)
#             self._updateInfo(c, checked)
#
#     def _onSmoothModeChanged(self, enable: bool):
#         self.scrollArea.setSmoothMode(SmoothMode(1 if enable else 0), Qt.Vertical)
#
#
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IconInterface()
    window.resize(810, 600)
    window.show()
    sys.exit(app.exec())